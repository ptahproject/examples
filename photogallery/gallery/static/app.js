define(
    'gallery', ['ptah', 'ptah-form', 'jquery', 'gallery-tmpls'],

    function(ptah, form, $, templates) {
        "use strict";

        return ptah.View.extend({
            __name__: 'PhotoGallery',
            connect: 'gallery',
            userid: null,
            username: null,
            loginwin: null,
            gallery: null

            , init: function() {
                ptah.connect()
            }

            , on_connect: function() {
                this.__dom__.append(templates.render('workspace'))
                this.workspace = $('[data-tag="workspace"]', this.__dom__)
                this.send('init')
            }

            , on_disconnect: function() {
                this.reset()

                this.menu_items.find(
                    '[data-tag="username"]').html('Guest')
                this.menu_items.find('[data-tag="login"]').show()
                this.menu_items.find('[data-tag="logout"]').hide()
                this.menu_items.find('[data-tag="menu"]').hide()
            }

            , msg_config: function(data) {
                this.config = data
                this.menu_items = $('[data-tag="topbar"]')
                new ptah.ActionChannel(this.menu_items, {scope: this})
            }

            , msg_loggedin: function(data) {
                this.userid = data.id
                this.username = data.name

                this.menu_items.find(
                    '[data-tag="username"]').html(this.username)
                this.menu_items.find('[data-tag="login"]').hide()
                this.menu_items.find('[data-tag="logout"]').show()
                this.menu_items.find('[data-tag="menu"]').show()
                try {
                    this.loginwin.destroy()
                } catch(e) {}

                this.send('list')
            }

            , msg_galleries: function(data) {
                this.gallery = null
                this.workspace.empty()
                this.workspace.append(templates.render('galleries', data))
            }

            , msg_gallery: function(data) {
                this.workspace.empty()
                this.workspace.append(templates.render('gallery', data))
            }

            , action_logout: function(options) {
                this.workspace.empty()
                this.menu_items.find(
                    '[data-tag="username"]').html('Guest')
                this.menu_items.find('[data-tag="login"]').show()
                this.menu_items.find('[data-tag="logout"]').hide()
                this.menu_items.find('[data-tag="menu"]').hide()
                this.send('logout')
            }

            , action_login: function(options) {
                var win = form.Window.extend({
                    template: templates.get('login'),
                    action_facebook: function() {
                        var config = this.__parent__.config
                        var top = screen.height?((screen.height-350)/2):150
                        var left = screen.width?((screen.width-750)/2):100
                        window.showModalDialog(
                            "https://www.facebook.com/dialog/oauth?client_id="
                                +config.facebook+
                                "&scope=email&display=popup&state=auth,"
                                +config.id+"&show_error=true&redirect_uri="
                                +ptah.gen_url('/_facebook_auth')
                            , null,
                            'dialogWidth:750px; dialogHeight=350px; '+
                                'dialogTop:'+top+'+px; dialogLeft:'+left+'px')
                    },
                    action_google: function() {
                        console.log('google')
                    },
                    action_github: function() {
                        console.log('github')
                    }
                })
                this.loginwin = new win(this)
            }

            , action_galleries: function() {
                this.send('list')
            }
            
            , action_addgallery: function() {
                new form.Form(this.connect, 'addgallery')
            }

            , action_editgallery: function(options) {
                new form.Form(this.connect, 'editgallery', {'id': options.id})
            }

            , action_removegallery: function(options) {
                var win = form.Window.extend({
                    template: templates.get('removegallery'),
                    action_confirm: function() {
                        this.destroy()
                        this.__parent__.send('removegallery', options)
                    }
                })
                new win(this)
            }

            , action_select_gallery: function(options) {
                this.gallery = options.id
                this.send('gallery', options)
            }

            , action_removephoto: function(options) {
                this.send('removephoto', options)
            }

            , action_uploadphoto: function(options) {
                var win = form.Window.extend({
                    template: templates.get('upload'),
                    action_confirm: function() {
                        this.destroy()
                    },

                    init: function(data) {
                        this._super()

                        this.dz = $('[data-tag="dropzone"]', this.__dom__)
                        this.dz.on({dragover: this.on_dragover,
                                    drop: this.on_drop}, this)
                    }
                    , on_dragover: function(ev) {
                        $(this).addClass('alert-success')
                        $(this).removeClass('alert-info')
                        return false
                    }
                    , on_drop: function(ev) {
                        var that = ev.data
                        $(this).addClass('alert-info')
                        $(this).removeClass('alert-success')
                        ev.preventDefault()
                        ev = ev.originalEvent || ev
                        
                        // upload files
                        var files = ev.files || ev.dataTransfer.files
                        if (files.length)
                            that.upload(files)
                        
                        return false
                    }

                    , upload: function(files) {
                        // upload files
                        var idx = 0
                        var form = this
                        var that = this.__parent__

                        var process_file = function() {
                            var file = files[idx]
                            var reader = new FileReader()
                            reader.onload = function (ev) {
                                if (file.type.slice(0, 6) === 'image/')
                                    that.send('upload',
                                              {id: options.id,
                                               data: reader.result,
                                               filename: file.name,
                                               mimetype: file.type})
                                idx += 1
                                if (idx < files.length) {
                                    process_file()
                                } else {
                                    form.destroy()
                                }
                            }
                            reader.readAsBinaryString(file)
                        }
                        process_file()
                    }
                })
                var upload = new win(this)
            }
        })
})
