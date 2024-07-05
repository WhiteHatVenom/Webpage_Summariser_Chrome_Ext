chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'summarize') {
    fetch('http://localhost:5001/summarize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: request.url }),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        const summary = data.summary;
        const dataUrl = 'data:text/plain;charset=utf-8,' + encodeURIComponent(summary);
        chrome.downloads.download({
          url: dataUrl,
          filename: 'blog_summary.txt',
          conflictAction: 'overwrite',
          saveAs: false,
        }, (downloadId) => {
          if (chrome.runtime.lastError) {
            console.error('Download failed:', chrome.runtime.lastError);
          } else {
            console.log('Summary downloaded successfully');
          }
        });
      })
      .catch(error => console.error('Error:', error));
  }
});