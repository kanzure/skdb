function showDialog(d) {
        d.show("slow");
}


function hideDialog(d) {
        d.hide("def");
}


function showStatus(msg, disappeartime) {
        if (disappeartime == undefined) {
                disappeartime = 2500;
        }
        $('#statusbox').text(msg);
        $('#statusbox').show("slow");
        $('#statusbox').animate({}, disappeartime).hide("def");
}


function hideStatus() {
        $('#statusbox').hide("def");
}


function showProgress(msg) {
        $('#progressmsg').text(msg);
        $('#progressbox').show("slow");
}


function hideProgress(msg) {
        $('#progressbox').hide("def");
}
