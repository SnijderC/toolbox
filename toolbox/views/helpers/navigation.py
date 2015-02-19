# -*- coding: utf-8 -*-
from toolbox.models import Category, ParentCategories, Platform, Formfactor, MainNav
from settings import slugs as sluglist, title as page_title
import copy

class Navigation(object):
    
    def __getitem__(self,item):
        """
            Make some variables easily accessable..
        """
        if item == "categories":
            return self.categories
        elif item == "platforms":
            return self.platforms
        elif item == "formfactors":
            return self.formfactors
        elif item == "sluglistrev":
            return self.sluglistrev
        else:
            return super(Navigation,self).__getitem__(item)
    

    def __init__(self,slugs):
        """
            Init navigation class, retrieves various settings and data from DB.
            
            Data from DB includes categories, platforms, formfactors etc.
            Other data provided includes the slug list from settings files.
            This data is also processed in reverse so you can do dict lookups.
            
            Furthermore.. 
             - Selected filters are calculated.
             - Lists of all category types are generated.
             - Menu structure for Navbar and Sitemap is generated (arrays/dicts
               not formatted)
             - Selected filters are preprocessed for display of deselection
               tags.
            
            The class also provides methods to generate URL's relating to
            categories or items in the DB. It has various presets that make 
            sure some settings are only singular, others accumulate, some replace
            others.
        """
        
        self.categories         = {}
        self.platforms          = {}
        self.sluglistrev        = {}
        self.navigation_items   = []
        self.navbar             = []
        self.sitemap            = []
        self.categorieslinks    = {}
        self.platformslinks     = {}
        self.formfactorslinks   = {}
        self.itemtypelinks      = {}
        
        self.slugs = "/"+str(slugs)
        
        # Process the selected filters.
        self.filters = self.process_slugs(slugs)

        # Reverse the sluglist so it can be used in – you guessed it – reverse!                
        for val in sluglist:
            self.sluglistrev[sluglist[val]['slug']] = copy.deepcopy(sluglist[val])
            self.sluglistrev[sluglist[val]['slug']]['slug'] = val
        
        # Retrieve the categories and other category types from the DB and make dicts out of them
        # also make some URL's to each one.
        self.categories, self.categorieslinks = self.getfilteritems(Category,"categories")
        self.platforms, self.platformslinks = self.getfilteritems(Platform,"platforms")
        self.formfactors, self.formfactorslinks = self.getfilteritems(Formfactor,"formfactors")      
        
        # setnavitems append items to the class attributes: navbar and sitemap
        self.navbar, self.sitemap = self.setnavitems()

        # Generate links for the page indexes (tools, advise)
        for key, val in enumerate(sluglist):
            if sluglist[val]['single']:
                self.itemtypelinks[val] = self.makelink(val)    

    def setnavitems(self):
        """
            Get the entire menu structure from the database (Navbar + Sitemap)
            
        """
        navbar = []
        sitemap = []
        
        """
            This is all about all the categories that are simple slugs..     
        """
        
        # all navigation items are related to this model
        objmainnav = MainNav.objects.select_related()
        
        for navitem in objmainnav:
            navbar.append({
                        'name'      : navitem.name,   
                        'icon'      : navitem.icon,
                        'children'  : [] 
                     })
            # make a short reference to the current menu item         
            navbarobj = navbar[-1]['children']
            
            # Loop through parentcategories and get the attributes..
            for parentcategory in navitem.categories.all():
                
                parentcategoryobj = {
                                'name'      : parentcategory.name,
                                'icon'      : parentcategory.icon,
                                'children'  : []
                            }
                if parentcategory.show_in_nav:
                    navbarobj.append(copy.deepcopy(parentcategoryobj))
                    navbargroup = navbarobj[-1]['children']
                if parentcategory.show_in_sitemap:
                    sitemap.append(parentcategoryobj)
                    sitemapgroup = sitemap[-1]['children']
                    # loop trough parentcategories' categories and get the attributes..
                    for category in parentcategory.categories.all():
                        categoryobj = {
                                        'name' : category.name,
                                        'icon' : category.icon,
                                        "href" : self.categories[category.slug]['href']
                                      }
                        if category.show_in_nav and parentcategory.show_in_nav:
                            navbargroup.append(copy.deepcopy(categoryobj))
                        if category.show_in_sitemap and parentcategory.show_in_sitemap:
                            sitemapgroup.append(categoryobj)
        
        """
            This is all about platforms and formfactor combinations..
            These are more complex combinations..
        """
        
        # all navigation items are related to this model
        objformfactor = Formfactor.objects.select_related()
        
        # make a short reference to the current menu item and add its references
        navbar.append({
                        'name'      : 'Platform',
                        'icon'      : 'tb-platforms',
                        'children'  : [] 
                      })
        # copy of navbar content..              
        #sitemap = copy.deepcopy(navbar)
        navbarobj  = navbar[-1]['children']
        #sitemapobj = sitemap[-1]['children']
        # Loop through formfactors and get the attributes..
        for formfactor in objformfactor.all():
            formfactorobj = {
                                'name'      : formfactor.name,
                                'icon'      : formfactor.icon,
                                'href'      : self.formfactors[formfactor.slug]['href'],
                                'children'  : []
                             }
            if formfactor.show_in_nav:
                navbarobj.append(copy.deepcopy(formfactorobj))
                navbargroup = navbarobj[-1]['children']
            if formfactor.show_in_sitemap:    
                sitemap.append(formfactorobj)
                sitemapgroup = sitemap[-1]['children']

            #loop trough formfactors' platforms and get the attributes..
            for platform in formfactor.platforms.all():
                #if platform.show_in_nav: this attribute does not exist, reason:
                #why would you exclude a platform?
                platformobj = {
                                'name' : platform.name,
                                'icon' : platform.icon,
                                'href' : self.makelink("formfactor/%s/platform/%s" % (formfactor.slug,platform.slug)),
                              }
                if formfactor.show_in_nav:
                    navbargroup.append(copy.deepcopy(platformobj))
                if formfactor.show_in_sitemap:
                    sitemapgroup.append(platformobj)
        
        # reorder the navbar to put Platform (which is now last) first
        navbar.insert(0,navbar.pop())

        return (navbar, sitemap)
        
    
    def getfilteritems(self,model,slug):
        """
            Generate a list of categories and links to those.
            
            Categories is not the same as what categories are called in the DB.
            Categories can also mean platforms, formfactors etc.
        """
        target = {}
        directlinks = {}
        
        # Dynamically select a category type
        obj_items = model.objects.all()

        # Alias to the reverse sluglist
        revslug = self.sluglistrev[slug]['slug']

        # Loop through all the items in the category type's table
        for item in obj_items:
            # Figure out what the direct link to this category is.. 
            directlinks[item.slug] = self.makelink("%s/%s" % (revslug, item.slug))
            # Add the direct link to a list, include it's name and ID too.
            target[item.slug] = {
                                  "name" : item.name,
                                  "id"   : item.id,
                                  "href" : directlinks[item.slug]
                                }
        # Return both lists independently
        return target, directlinks
    
    def filter_tags(self):
        """
            Generate a list of selected filters to be displayed 
            as tags on the index page.
        """
        
        # Alias some variables for easy access
        revnewslug      = self.sluglistrev        
        req             = self.slugs
        filters         = self.filters
        # Place holder
        obj_filters     = []
        
        # Loop through all filters
        for strslug in filters:
            # We don't want these for main selection (tools, advise)
            if strslug not in ("item_slug","item_arg"):
                # If one of these is a match set specific class, 
                # might be better to move to the CSS/LESS file instead.
                if strslug == "categories":
                    strclass = "category"
                elif strslug == "formfactors":
                    strclass = "light-bulb"
                # Or use the slug as the class
                else:
                    strclass = strslug
                
                # For each selection under a slug that may or may not be multiple
                # Add an item to the list.
                args  = filters[strslug]                  
                for strarg in args:
                    obj_filters.append({ 
                            'class': 'tb-%s' % strclass,
                            'text' : self[strslug][strarg]['name'],
                            'href' : req.replace("%s/%s/" % (revnewslug[strslug]['slug'],strarg) ,""),
                          })
    
        return obj_filters
           
    def makelink(self,slugstr):
        # Alias the currently selected filters.
        oldslugs    = self.filters
        # Process slugstring into the filters that belong to the link that we 
        # are creating.
        linkslugs   = self.process_slugs(slugstr)
        
        # Make a complete copy of the current filters.
        newslugs    = copy.deepcopy(oldslugs)
                        
        link = ""
        
        # For each of the new slugs check if set or not,
        # if set, add/replace in the copy of the old one.
        for slug in linkslugs:
            if linkslugs[slug]:
                newslugs[slug] = linkslugs[slug]        
        
        # Now compile the list of slugs and arguments into a url.
        for slug in newslugs:
            # These 2 slugs should be handled differently..
            if slug not in ("item_slug","item_arg"):
                # We need the user version of the slug, not the DB one.
                slugrev = self.sluglistrev[slug]['slug']
                # Add the user version slug and argument to the url
                for arg in newslugs[slug]:
                    link += '/%s/%s' % (slugrev , arg)
            # New links will forget item_arg which is a single item..
            elif slug == "item_slug":
                """
                    This should be used to stay in the same layout
                    layout = self.sluglistrev[newslugs[slug]]['slug']
                    this is deemed to complicated behaviour for average users
                    always direct back to overview unless specifically chosen..
                """
                if linkslugs[slug]:
                    # specifically chosen..
                    layout = self.sluglistrev[linkslugs[slug]]['slug']
                else:
                    # not specifically chosen..
                    layout = "overzicht"
                # item_slug should come first..
                link = '/%s%s'  % (layout,link)
        link +='/'
        return link

    
    def process_slugs(self,slugs=""):
        """
            Make filter for orm request taking slugs as input.
            
            There are 2 types of slugs, those that need another slug as a keyword
            and those that do not need one. Loop through the slugs and return the
            sets or single slugs.
            
            Some slugs are of the "single" type, those can be queried with or without
            a keyword. There can be only one specified. This is not checked but only
            the last that is mentioned will be valid.
                
            1. Split the string into all the slugs found in the slugs.
            2. Temporarily store the "key" and "value" in the arr_filters object.
               Check whether the slug belongs in the "key" or "value" placeholder.
               If the string is mentioned in settings.views.slugs it's a key.
               These values SHOULD not be in the slugs of the database but are
               not currently validated..
            3. If a "key" slug is found, store it IF:
                a. The next slug is not a key (it's a value), then also store the value
                b. The next slug is also a key but the current slug is a "single" key
        
        
        """
        arr_filters = {}
        arr_filters['item_slug'] = ""
        arr_filters['item_arg']  = ""
        
        if slugs:
            
            arr_slugs = slugs.strip("/").split("/")
            
            arr_slugs_enum = enumerate(arr_slugs)
            
            for i, slug in arr_slugs_enum:
                if slug in sluglist.keys():

                    # find the database slugname..
                    slugrev = sluglist[slug]['slug']                    
                    
                    # peek in next value to see if this is a keyword.. 
                    if i < len(arr_slugs)-1 and arr_slugs[i+1] not in sluglist.keys():
                                
                        # if only one occurance may exist..
                        if sluglist[slug]['single']: # there can be only one..
                            arr_filters['item_slug'] = slugrev
                            arr_filters['item_arg']  = arr_slugs[i+1]
                        else:
                            # if this key does not yet exist make it an array..
                            if slugrev not in arr_filters.keys():
                                arr_filters[slugrev] = []
                            # if multiple occurances should accumulate..    
                            if sluglist[slug]['multiple']:
                                # add the value to the array
                                arr_filters[slugrev].append(arr_slugs[i+1])
                            else:
                                # replace the array
                                arr_filters[slugrev] = [arr_slugs[i+1]]
                            
                        # skip the next "slug" since it's not a slug, it's the value..
                        [ next(arr_slugs_enum) ]
                    elif sluglist[slug]['single']: # there can be only one..
                        arr_filters['item_slug'] = slugrev
                        continue
                    else:
                        continue

        return arr_filters        
        
        