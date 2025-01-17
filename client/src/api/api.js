async function Api(url, method, body={}){
  const header = {
    "Content-Type": "application/json"
  }
  try{
    const access_token=sessionStorage.getItem("user")["access_token"];
    const id_token=sessionStorage.getItem("user")["id_token"];
    const user_id=sessionStorage.getItem("user")["user_id"];
    header["access_token"]=access_token;
    header["id_token"]=id_token;
    header["user_id"]=user_id;
  }catch(error){}
  
  try{
    const request = {
      method: method,
      headers: header
    }
    if (method==="POST"){
      request["body"]=JSON.stringify(body)
    }
    const response = await fetch(url, );
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