"use strict";

jca.ns('ex');

ex.Chat = function(ca, container) {
    this.jca = ca
    this.container = container
    this.users = {}
    this.logger = jca.getLogger('ex.Chat');

    this.conn = new jca.Connection(
        '//'+window.location.host+'/ws-chat', this,
        {autoconnect: true,
         logger: this.logger}
    )
};

ex.Chat.prototype = {
    toString: function() {
        return "ex.Chat"
    },

    on_connect: function() {
        var conn = this.conn;
        this.container.append(this.templates.render('list'));
        this.ws = $('#internal-chat');
        conn.send('init');

        this.ws.delegate('div.btn', 'click', this, this.on_user_click);
    },

    on_disconnect: function() {
    },

    on_message: function(data, msg) {
        var type = msg.data['type'];
        if (type==='message') {
            var win = this.users[data['uid']];
            if (win) {
                win.msg_message.call(win, data);
            }
        }
    },

    msg_list: function(data) {
        this.uid = data.uid;
        this.name = data.name;

        var users = data.users;
        for (var idx=0; idx < users.length; idx++) {
            var item = users[idx];
            this.users[item.uid] =
                new ex.ChatWindow(this, item.uid, item.name);
        };
    },

    msg_joined: function(data) {
        if ((this.uid == data.uid) ||
            (this.users[data.uid]))
            return;

        this.users[data.uid] =
            new ex.ChatWindow(this, data.uid, data.name);
    },

    msg_disconnected: function(data) {
        if (this.users[data.uid]) {
            this.users[data.uid].remove();
            delete this.users[data.uid];
        }
    },

    on_user_click: function(ev) {
        var that = ev.data;
        var uid = $(this).parent().attr('id').slice(4);
        if (that.users[uid]) {
            that.users[uid].on_click();
        };
    }
};


ex.ChatWindow = function(manager, uid, user) {
    this.manager = manager;
    this.templates = manager.templates;
    this.logger = manager.logger;
    this.uid = uid;
    this.user = user;
    this.data = {uid: uid, name: user};
    this.window;
    this.window_hidden = true;

    this.manager.ws.append(this.templates.render('user', this.data));
    this.item = $('#item'+this.uid, this.manager.ws);
    this.indicator = $('div.pull-left i', this.item);

    $('body').append(this.templates.render('window', this.data));
    this.window = $('#window'+this.uid);
    this.messages = $('.messages', this.window);

    var self = this;

    var textarea = $('textarea[name="message"]', this.window);
    textarea.keypress(function(ev) {
        /* get keycode depending on IE vs. everyone else */
        var keynum = (window.event) ? event.keyCode : ev.keyCode;

        /* only interested in SHIFT */
        if (!ev.shiftKey) {
            switch(keynum) {
            case 13:  /* enter key */
                if ($(this).val())
                    self.send_message($(this));
                else
                    self.logger.info("Can't send empty message")
                ev.preventDefault();
                break;
            }
        }
    });

    this.window.on('shown', function() {
        textarea.focus();
        self.window_hidden = false;
        self.messages.animate({scrollTop: self.messages.height()});
    });

    this.window.on('hidden', function() {
        self.window_hidden = true;
    });
};


ex.ChatWindow.prototype = {
    toString: function() {
        return 'ex.ChatWindow<'+this.uid+'>';
    },

    remove: function() {
        this.window.modal('hide');
        this.window.remove();
        this.item.remove();
    },

    on_click: function() {
        this.window.modal();
        this.hide_incoming_msg();
    },

    show_incoming_msg: function() {
        this.indicator.removeClass();
        this.indicator.addClass('icon-comment');
    },

    hide_incoming_msg: function() {
        this.indicator.removeClass();
        this.indicator.addClass('icon-user');
    },

    send_message: function(el) {
        var msg = el.val();

        // append message
        this.messages.append(
            this.templates.render('message',
                                  {name: this.manager.name,
                                   message: msg,
                                   date: jca.utc()})
        );
        this.messages.animate({scrollTop: this.messages.height()});

        this.manager.conn.send('message', {uid: this.uid, message: msg})
        el.val('');
    },

    msg_message: function(data) {
        var tmpl = this.templates['message'];
        this.messages.append(this.templates.render('message', data));
        this.messages.animate({scrollTop: this.messages.height()});

        if (this.window_hidden) {
            this.show_incoming_msg();
        }
    }
};
