define(
    'settings', ['jca', 'jquery'],

    function(jca, $) {
        "use strict";

        var Settings = jca.component('settings', {
            __templates__: 'ptah_ws:settings'

            , init: function() {
                this.data = {}
                this.logger = jca.get_logger('settings')
                this.register_with_connection()
            }
            
            , destroy: function() {
                this.container.empty()
            }

            , set_navitem: function(name) {
                $('[data-place="nav"] li', this.container).each(function() {
                    var el = $(this)
                    el.removeClass('active')
                    $('i', el).addClass('icon-white');
                });

                var item = $('li[data-navitem="' + name + '"]', this.container);
                item.addClass('active');
                var i = $('i', item);
                i.removeClass('icon-white');
            }

            , on_connect: function() {
                this.container.append(this.templates.render('workspace'))
                this.workspace = $('[data-place="workspace"]', this.container)
                this.send('init')
            }

            , action_activate: function(options) {
                this.set_navitem(options.name)
                this.workspace.empty()
                this.workspace.append(
                    this.templates.render(
                        'group', this.data[options.name.substr(9)]))
            }

            , action_modify: function(options) {
                new jca.Form(
                    this, 'group_edit', {'__group__': options.name},
                    {width: (options.name === 'app') ? '650px' : '500px'} )
            }

            , msg_list: function(data) {
                this.data = data['settings']
                this.action_activate({name: 'settings-ptah-ws'})
            }

            , msg_updated: function(data) {
                var name = data['name']
                this.data[name] = data
                this.action_activate({name: 'settings-'+name})
            }
        })

        return Settings
    }
)
