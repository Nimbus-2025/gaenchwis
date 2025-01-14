async function Api(url, method, body){
  try{
    const access_token=sessionStorage.getItem("user")["access_token"];
    const id_token=sessionStorage.getItem("user")["id_token"];
    body["access_token"]=access_token;
    body["id_token"]=id_token;
  }catch(error){}
  
  try{
    const response = await fetch(url, {
      method: method,
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    });
    return await response.json();
  } catch(error){
    console.error(error);
    return error;
  }
  
}

function invalid_login(){
  sessionStorage.clear();
}

export default Api;