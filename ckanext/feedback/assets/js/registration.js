function checkTitleAndDescriptionExists() {
  const title = document.getElementById('title').value;
  const description = document.getElementById('description').value;
  const titleErrorMessage = document.getElementById('title-error');
  const descriptionErrorMessage = document.getElementById('description-error');

  // Reset display settings
  titleErrorMessage.style.display = 'None';
  descriptionErrorMessage.style.display = 'None';
  
  if (!title) {
    titleErrorMessage.style.display = '';
    return false;
  }
  if (!description) {
    descriptionErrorMessage.style.display = '';
    return false;
  }
  return true;
}