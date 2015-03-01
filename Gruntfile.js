'use strict';
// Default live reload port, used by most plugins.
var LIVERELOAD_PORT = 35729;
// Commented is disabled because it's not used, resulting in a smaller JS file
var JAVASCRIPT_CONCAT = [
                            'vendors/jquery/dist/jquery.js',
//                            'vendors/bootstrap/js/affix.js',
//                            'vendors/bootstrap/js/alert.js',
                            'vendors/bootstrap/js/button.js',
//                            'vendors/bootstrap/js/carousel.js',
                            'vendors/bootstrap/js/collapse.js',
                            'vendors/bootstrap/js/dropdown.js',
//                            'vendors/bootstrap/js/modal.js',
//                            'vendors/bootstrap/js/scrollspy.js',
//                            'vendors/bootstrap/js/tab.js',
                            'vendors/bootstrap/js/tooltip.js',
                            'vendors/bootstrap/js/popover.js',
                            'vendors/bootstrap/js/transistion.js',
                            'vendors/typeahead.js/dist/typeahead.bundle.js',
                            'toolbox/js/index.js'
                        ];
module.exports = function (grunt) {
    // load all grunt tasks
    require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);

    grunt.initConfig({
        /* 
        // Setup a watch task to watch file changes in several folders.
        // You can set the LESS and CSS files so that it quickly compiles those
        // when you make changes but you can also list other files that change
        // the layout or content to auto-reload the page. (Requires a plugin or
        // a live reload script, batteries not included.)
        */
        watch: {
            options: {
                nospawn: false
            },
            // The actual live reload server.. 
            livereload: {
                options: {
                    livereload: LIVERELOAD_PORT
                },
                files: [
                    'toolbox/*.py',
                    'toolbox/models/*.py',
                    'toolbox/views/{,*/}*.py',
                    'toolbox/templates/{,*/}*.jade',
                    'toolbox/templates/{,*/}*.md',
                    'toolbox/static/css/index.css',
                    'toolbox/static/js/index.js'  
                ]
            },
            js:
            {
                files: ['toolbox/js/*.js'],
                tasks: ['concat:server']
            },
            less: {
                files: ['toolbox/less/*.less'],
                tasks: ['less:server']
            }
        },
        /*
        // Compile LESS to CSS files, for build it does a little bit more work
        // for compression which takes more time. Build reports the size delta too.
        */
        less: {
            server: {
                options: {
                    paths: ['vendors/bootstrap/less', 'toolbox/less']
                },
                files: {
                    'toolbox/static/css/index.css': ['toolbox/less/index.less'],
                    'toolbox/static/css/error.css': ['toolbox/less/error.less']
                }
            },
            build: {
                options: {
                  cleancss: true,
                  report: 'min',
                  paths: ['vendors/bootstrap/less', 'toolbox/less']
                },
                files: {
                    'toolbox/static/css/index.css': ['toolbox/less/index.less'],
                    'toolbox/static/css/error.css': ['toolbox/less/error.less']
                }
              },
        },
        // Concat the JS files used for both the server as well as the build task
        concat: {
            server: {
                src: JAVASCRIPT_CONCAT,
                dest: 'toolbox/static/js/index.js'
            },
            build: {
                src: JAVASCRIPT_CONCAT,
                dest: 'toolbox/js/concat/index.js'
            }
        },
        // Uglify the JS files to make them as small as possible..
        uglify: {
           build: {
             files: {
               'toolbox/static/js/index.js': ['toolbox/js/concat/index.js']
             }
           }
        },
        // Compare the before and after size, useful for measuring the size with or without dependencies
        // as well as before and after compression
        compare_size: {
			files: [ "toolbox/js/concat/index.js", "toolbox/static/js/index.js" ],
			options: {
				cache: ".sizecache.json"
			}
		},
    });

    // Register a grunt task for livereloading and fast compiling (compile LESS, concat JS)
    grunt.registerTask('server', function (target) {

        grunt.task.run([
            'less:server',
            'concat:server',
            'compare_size',
            'watch'
        ]);
    });
    
    // Register a grunt task for building (compile LESS, concat JS, compress and uglify, show size delta)    
    grunt.registerTask('build', function (target) {

        grunt.task.run([
            'less:build',
            'concat:build',
            'uglify:build',
            'compare_size',
        ]);
    });
};
