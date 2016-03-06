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


function orderQuestions() {
    var $fieldset = $('#fs'),
        $fieldsetdiv = $fieldset.children('div.form-group');

    $fieldsetdiv.sort(function(a,b){
        var an = parseInt(a.getAttribute('order')),
            bn = parseInt(b.getAttribute('order'));

        if(an > bn) {
            return 1;
        }
        if(an < bn) {
            return -1;
        }
        return 0;
    });

    $fieldsetdiv.detach().appendTo($fieldset);
}

function upload_files_click(form_id) {
    var field_name = 'id_form-' + form_id + '-files';
    //alert(field_name);
    elem = document.getElementById(field_name);
    elem.click()
}

function setFocusFirstElemForm(){
  if(document.forms){
     form = document.forms[0];
     if(form){
        if(form.elements){
            for(i=0; i<form.length;i++){
               if(form[i].readOnly == false && form[i].type != 'hidden'){
                    form[i].focus();
                    form[i].select();
                    return;
               }
            }
        }
     }
  }
}