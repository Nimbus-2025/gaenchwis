function LoginfromChromeExtension() {
  if (!sessionStorage.getItem('user')){
    const handleMessage = (event) => {
      if (event.source !== window || !event.data.type) return;
      if (event.data.type === "web_login_response" && event.data.success){
        const user = {
          phone: event.data.data.phone,
          email: event.data.data.email,
          name: event.data.data.name,
          access_token: event.data.data.access_token,
          id_token: event.data.data.id_token,
          user_id: event.data.data.user_id
        }
        sessionStorage.setItem('user', JSON.stringify(user));
      }
    };
    
    window.addEventListener("message", handleMessage);
    setTimeout(() => {
      window.postMessage({ type: "web_login_request" }, "*");
    }, 2000);
  }
};

export default LoginfromChromeExtension;
