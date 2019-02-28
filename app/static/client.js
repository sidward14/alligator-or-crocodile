var el = x => document.getElementById( x );

// ########################################################################## //

function confirmOverUpload( inputID ) { el('choose-file-button').style.backgroundColor = '#C7C5F6'; }

function confirmOverClassify( inputID ) { el('classify-button').style.color = '#7A49EC'; }

function confirmOutUpload( inputID ) { el('choose-file-button').style.backgroundColor = '#ffffff'; }

function confirmOutClassify( inputID ) { el('classify-button').style.color = '#ffffff'; }

function showPicker( inputId ) { el('file-input').click(); }

function showPicked( input ) {
  el('upload-label').innerHTML = input.files[0].name;
  var reader = new FileReader();
  reader.onload = function (e) {
    el('image-picked').src = e.target.result;
    el('image-picked').className = '';
  }
  reader.readAsDataURL( input.files[0] );
}

function analyze() {
  var uploadFiles = el('file-input').files;
  if (uploadFiles.length != 1) alert('Please select 1 file to analyze!');

  el('classify-button').innerHTML = 'Analyzing...';
  var xhr = new XMLHttpRequest();
  var loc = window.location
  xhr.open( 'POST', `${loc.protocol}//${loc.hostname}:${loc.port}/classify`, true );
  xhr.onerror = function() {alert (xhr.responseText);}
  xhr.onload = function( e ) {
    if (this.readyState === 4) {
      var response = JSON.parse( e.target.responseText );
      el('result-label').innerHTML = `prediction: ${ response.result }`;
    }
      el('classify-button').innerHTML = 'Classify!';
  }

  var fileData = new FormData();
  fileData.append( 'file', uploadFiles[0] );
  xhr.send( fileData );
}
