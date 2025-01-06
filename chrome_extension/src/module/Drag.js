chrome.runtime.onInstalled.addListener(() => {
  function createContextMenus() {
    chrome.storage.local.get(null, (result) => {
      const title = result.title || [];
      const content = result.content || [];
      
      chrome.contextMenus.removeAll(() => {
        for (let i = 1; i < title.length+2; i++) {
          let menus_title=i + "번 자기소개서 문항 수정";
          if (i === title.length+1){
            menus_title=i + "번 자기소개서 문항 저장";
          }
          chrome.contextMenus.create({
            id: 'title_'+i,
            title: menus_title,
            contexts: ["selection"]
          });
        }
        for (let i = 1; i < title.length+1; i++) {
          let menus_title=i + "번 자기소개서 내용 수정";
          if (content[i-1] === null) {
            menus_title=i + "번 자기소개서 내용 저장";
          }
          chrome.contextMenus.create({
            id: 'content_'+i,
            title: menus_title,
            contexts: ["selection"]
          });
        }
      });
    });
  }

  createContextMenus();

  chrome.storage.onChanged.addListener((changes, namespace) => {
    if (namespace === 'local' && (changes.title || changes.content)) {
      createContextMenus();
    }
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: (type, text) => {
      chrome.storage.local.get(null, (result) => {
        const title = result.title || [];
        const content = result.content || [];

        const [input_type, id] = type.split('_')

        if (input_type === "title") {
          title[Number(id)-1]=text;
          if (content[Number(id)-1] === undefined){
            content[Number(id)-1]=null
          }
          chrome.storage.local.set({ title: title, content: content });
        }
        else{
          content[Number(id)-1]=text;
          chrome.storage.local.set({ content: content });
        }
      });
    },
    args: [info.menuItemId,info.selectionText]
  });
});