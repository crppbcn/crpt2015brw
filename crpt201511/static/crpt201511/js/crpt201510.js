function setFocusFirstElemForm(){
  if(document.forms){
     form = document.forms[0];
     if(form){
        if(form.elements){
            for(i=0; i<form.length;i++){
               if(form[i].readOnly == false && form[i].type != 'hidden'){
                        form[i].focus();
                        return;
               }
            }
        }
     }
  }
}


function setUploadButtonAssessment(){
  file_element = document.getElementById("id_form-0-file");
  if (file_element){
        file_element.onchange = function () {
        document.getElementById("labelFile").value = file_element.value;
        document.getElementById("linkFile").style.display='none';
        document.getElementById("labelFile").style.display='inline';
      };
      document.getElementById("chooseFile").onclick = function() {
        file_element.click();
      }
  }
}








