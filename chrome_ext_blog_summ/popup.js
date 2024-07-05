document.getElementById('summarizeButton').addEventListener('click', async () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.scripting.executeScript(
        {
          target: { tabId: tabs[0].id },
          function: () => window.location.href
        },
        (results) => {
          const url = results[0].result;
          chrome.runtime.sendMessage({ action: 'summarize', url: url });
        }
      );
    });
  });
  