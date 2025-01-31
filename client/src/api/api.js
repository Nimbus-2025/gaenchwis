async function Api(url, method, body = {}) {
  const header = {
    'Content-Type': 'application/json',
  };
  try {
    const data = JSON.parse(sessionStorage.getItem('user'));
    const access_token = data.access_token;
    const id_token = data.id_token;
    const user_id = data.user_id;
    header['access_token'] = access_token;
    header['id_token'] = id_token;
    header['user_id'] = user_id;
  } catch (error) {}

  try {
    const request = {
      method: method,
<<<<<<< HEAD
      headers: header,
    };
    if (method === 'POST' || method === 'PATCH') {
      request['body'] = JSON.stringify(body);
=======
      headers: header
    }
    if (method!=='GET' && method!=='HEAD'){
      request["body"]=JSON.stringify(body)
>>>>>>> a5e13d0 (fix: 캘린더 일정 수정 ver0.9)
    }

    const response = await fetch(url, request);

    return await response.json();
  } catch (error) {
    console.error(`${url}, ${error}`);
    return error;
  }
}

function invalid_login() {
  sessionStorage.clear();
}

export default Api;
