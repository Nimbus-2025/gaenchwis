function LoginfromChromeExtension() {
  if (!sessionStorage.getItem('access_token')){
    const handleMessage = (event) => {
      if (event.source !== window || !event.data.type) return;
      if (event.data.type === "web_login_response" && event.data.success){
        console.log(event.data.success)
        console.log("Response from extension:", event.data);
        const user = {
          email: event.data.data.email,
          name: event.data.data.name,
          access_token: event.data.data.access_token,
          id_token: event.data.data.id_token
        }
        sessionStorage.setItem('user', user);
      }
    };
    
    window.addEventListener("message", handleMessage);
    setTimeout(() => {
      window.postMessage({ type: "web_login_request" }, "*");
    }, 2000);
  }
};

export default LoginfromChromeExtension;
