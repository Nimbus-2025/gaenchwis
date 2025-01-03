chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.get(null, (result) => {
    const essay = result.essay || {};
    const essay_titles = Object.keys(essay);
    const new_essay_title_num = essay_titles.length+1;

    chrome.contextMenus.create({
      id: "dragTitle",
      title: new_essay_title_num+"번 자기소개서 문항 저장",
      contexts: ["selection"]
    });
    for (let i=1; i<new_essay_title_num; i++){
      if (essay[essay_titles[i]] === null){
        chrome.contextMenus.create({
          id: i,
          title: i+"번 자기소개서 내용 저장",
          contexts: ["selection"]
        });
      }
    }
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: (type, text) => {
      chrome.storage.local.get(null, (result) => {
        const essay = result.essay || {};
        if (type === "dragTitle") {
          essay[text]=null
          chrome.storage.local.set({ essay: essay })
        }
      });
    },
    args: [info.menuItemId,info.selectionText]
  });
});