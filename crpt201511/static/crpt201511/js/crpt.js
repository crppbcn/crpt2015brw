function showConsiderations() {
    $("#crpt-right-considerations").show()
    $('#a-considerations').css('color','#3D6FB6');
    $('#crpt-right-comments').hide();
    $('#a-comments').css('color','#EE8A00');
}

function showComments() {
    $('#crpt-right-considerations').hide();
    $('#a-considerations').css('color','#EE8A00');
    $('#crpt-right-comments').show();
    $('#a-comments').css('color','#3D6FB6');
}

$(document).ready(function () {
    $('#crpt-right-comments').hide();
    $("#divMoVOther").hide();
    $('#select2').change(function(){
        $("#select2 option:selected").each(function() {
            if ($(this).text() == 'Other'){
               $("#divMoVOther").show();
               return;
            }
           $("#divMoVOther").hide();
        });
    });
})

function copyComments() {
    $('#textEmail').val($('#textComments').val());
}