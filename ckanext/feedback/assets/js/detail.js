function checkCommentExists() {
  errorElement  = document.getElementById('content-error');
  content = document.getElementById('comment-content').value;

  if (content) {
    errorElement.style.display = 'None';
    return true;
  } else {
    errorElement.style.display = '';
    return false;
  }
}