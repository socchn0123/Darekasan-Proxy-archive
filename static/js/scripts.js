document.getElementById('urlForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var url = document.getElementById('url').value;
    fetch('/proxy', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        if (data.https_failed) {
            showConfirmationDialog(data.url);
        } else {
            addTab(data.saved_path, data.title);
        }
    });
});

function showConfirmationDialog(url) {
    var dialog = document.getElementById('confirmationDialog');
    dialog.style.display = 'block';

    document.getElementById('confirmYes').onclick = function() {
        dialog.style.display = 'none';
        url = url.replace('https://', 'http://');
        addTab(url, 'No Title');
    };

    document.getElementById('confirmNo').onclick = function() {
        dialog.style.display = 'none';
    };
}

function addTab(url, title) {
    var tabs = document.getElementById('tabs');
    var tabContents = document.getElementById('tabContents');

    var tabLink = document.createElement('button');
    tabLink.className = 'tablink';
    tabLink.textContent = title;
    tabLink.onclick = function() {
        openTab(event, url);
    };

    var closeButton = document.createElement('button');
    closeButton.className = 'closeButton';
    closeButton.textContent = '×';
    closeButton.onclick = function() {
        removeTab(url);
    };

    var tabContainer = document.createElement('div');
    tabContainer.className = 'tabContainer';
    tabContainer.appendChild(tabLink);
    tabContainer.appendChild(closeButton);
    tabs.appendChild(tabContainer);

    var tabContent = document.createElement('div');
    tabContent.id = url;
    tabContent.className = 'tabcontent';
    var iframe = document.createElement('iframe');
    iframe.src = url;
    iframe.width = '100%';
    iframe.height = '600px';
    tabContent.appendChild(iframe);
    tabContents.appendChild(tabContent);

    tabLink.click();
}

function removeTab(url) {
    var tabContainer = document.querySelector(`.tabContainer button[onclick="openTab(event, '${url}')"]`).parentElement;
    var tabContent = document.getElementById(url);
    tabContainer.remove();
    tabContent.remove();

    // デフォルトで最初のタブを開く
    if (document.getElementsByClassName('tablink').length > 0) {
        document.getElementsByClassName('tablink')[0].click();
    }
}

function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName('tabcontent');
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = 'none';
    }
    tablinks = document.getElementsByClassName('tablink');
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(' active', '');
    }
    document.getElementById(tabName).style.display = 'block';
    evt.currentTarget.className += ' active';
}

// デフォルトで最初のタブを開く
if (document.getElementsByClassName('tablink').length > 0) {
    document.getElementsByClassName('tablink')[0].click();
}
