function select(e){
    var pick_str = document.pick_info.pick_str.value;
    if(pick_str.indexOf(e.name) != -1){
        return;
    }
    else{
        var hero_img = e.getElementsByTagName("img")[0];

        var pick = document.getElementById("pick_seq");
        pick.appendChild(hero_img.cloneNode(true));
        if(document.pick_info.pick_str.value == ""){
            document.pick_info.pick_str.value = e.name;
        }
        else{
            document.pick_info.pick_str.value += ":" + e.name;
        }
        document.pick_info.submit();
    }
}

function undo(e){
    var picks = document.getElementById("pick_seq");
    var icons = picks.getElementsByTagName("div");
    var len = icons.length;
    if(len != 0){
        picks.removeChild(icons[len-1]);
    }

    var key_str = document.pick_info.pick_str.value;
    var keys = key_str.split(":")
    keys.pop();
    document.pick_info.pick_str.value = keys.join(":");
    document.pick_info.submit();
}

function reset(e){
    var picks = document.getElementById("pick_seq");
    while (picks.firstChild) picks.removeChild(picks.firstChild);
    var reset_button = e.cloneNode(true);
    document.pick_info.pick_str.value = "";
    document.pick_info.submit();
}
