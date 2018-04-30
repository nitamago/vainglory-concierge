function submmit(e){
    var content = CKEDITOR.instances.editor.getData();
    var form = document.forms.article_info;
    form.content.value = content;
    document.article_info.submit();
}
