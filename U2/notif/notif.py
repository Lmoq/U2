import os

def termux_notif( follow_default=True, **kwargs ):
    k_args = kwargs
    
    if follow_default:
        default_id = 21
        dict_ = {
            "--id"      : default_id,
            "--title"   : "Notification",
            "--priority" : "medium",
        }
        dict_.update(kwargs)
        k_args = dict_

    cm = "termux-notification "

    for k,v in k_args.items():
        cm += f"{k} {v} "

    os.system(cm + '&')


def notif( pin=True, fd=True, include_exit_button = True, **d ):
    global follow_default
    
    follow_default = fd
    kwargs = d
    
    termux_keymap = {
        "title" : "--title",
        "content" : "-c",
        "id" : "-id",
        "b1" : "--button1",
        "b2" : "--button2",
        "b3" : "--button3",
        "action" : "--action",
        "b1_action" : "--button1-action",
        "b2_action" : "--button2-action",
        "b3_action" : "--button3-action",
        "img" : "--image-path",
    }

    # Replaces the simplified keys from arguments with the 
    # corresponding termux notification args
    def getCorrectKeys( kwargs, src ):
        out = {}
        for simplified, real_key in src.items():
            value = kwargs.get( simplified )
            if value: 
                out[ real_key ] = f"'{value}'"
        return out

    result = getCorrectKeys( kwargs, termux_keymap )

    if include_exit_button:
        result['--button3'] = "'Exit'"
        result['--button3-action'] = "'termux-notification-remove 21'"
    if pin : result['--ongoing'] = ''

    termux_notif( fd, **result )

if __name__=='__main__':
    pass
