var MarkdownEditor = (function() {

  var init = function() {
    // markdown parser configuration
    marked.setOptions({
      gfm: true,
      tables: true,
      breaks: true,
      pedantic: false,
      sanitize: false,
      smartLists: true,
      langPrefix: 'language-',
      highlight: function(code, lang) {
        if (lang) {
          return hljs.highlight(lang, code).value || code;
        }

        return hljs.highlightAuto(code).value || code;
      }
    });

    // javascript support
    var classNames = document.body.className.split(' ');
    if (window.FileReader) {
      classNames.push('filereader');
    }
    if (window.saveAs && window.Blob) {
      classNames.push('filesaver');
    }
    document.body.className = classNames.join(' ');

    // source & preview
    var source = document.getElementById('editor_code');
    var output = document.getElementById('preview_code');

    // events
    source.onkeydown = function(event) {
      var keyCode = event.keyCode ? event.keyCode : event.charCode ? event.charCode : event.which;
      if (keyCode == 9 && !event.shiftKey && !event.ctrlKey && !event.altKey) {
        var scrollTop = this.scrollTop;

        if (this.setSelectionRange) {
          var selectionStart = this.selectionStart;
          var selectionEnd = this.selectionEnd;
          this.value = this.value.substring(0, selectionStart) + '\t' + this.value.substr(selectionEnd);
          this.setSelectionRange(selectionStart + 1, selectionStart + 1);
          this.focus();
        } else if (this.createTextRange) {
          document.selection.createRange().text = '\t';
          event.returnValue = false;
        }

        this.scrollTop = scrollTop;

        if (event.preventDefault) {
          event.preventDefault();
        }

        return false;
      }

      return true;
    };

    source.onchange = source.onkeyup = function() {
      var html = marked(this.value);
      output.innerHTML = '<div class="markdown-body">'+html+'</div>';
    }

    source.onchange();
  };

  var open = function() {
    var container = document.getElementById('file_container');
    var input = document.getElementById('file');
    var source = document.getElementById('editor_code');
    var event = document.createEvent('MouseEvents');
    event.initEvent('click', true, false);
    input.dispatchEvent(event);

    input.onchange = function() {
      var fileName = this.value, fileObject = this.files[0], reader = new FileReader();

      reader.onloadend = function(e) {
        source.value = e.target.result;
        source.onchange();
        container.innerHTML = '<input type="file" id="file" name="file" />';
      };
      reader.onerror = function() {
        alert('Error reading file: ' + fileName);
        container.innerHTML = '<input type="file" id="file" name="file" />';
      };

      reader.readAsText(fileObject);
    };
  };

  var saveMd = function() {
    var blob = new Blob([ document.getElementById('editor_code').value ], { type: "text/x-markdown; charset=UTF-8" });
    window.saveAs(blob, "Source.md");
  };
  var saveHtml = function() {
    var blob = new Blob([ document.getElementById('preview_code').innerHTML ], { type: "text/html; charset=UTF-8" });
    window.saveAs(blob, "Preview.html");
  };

  return {
    init      : init,
    open      : open,
    saveMd    : saveMd,
    saveHtml  : saveHtml
  };

})();
