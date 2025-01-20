import React, { useState, useEffect } from 'react';
import PickImage from '../image/pick.png'
import EssayLoadImage from '../image/essayload.png'
import SaveImage from '../image/save.png'
import HrefImage from '../image/href.png'
import '../style/post.css';
import "../style/icon.css";
import LoadEssayList from './LoadEssayList';

function Post({postData, post_id}) {
  const [pick, setPick]=useState(false);
  const [loadDragEssay, setLoadDragEssay]=useState(false);
  const [loadDragData, setLoadDragData]=useState(null);
  const [data, setData]=useState(postData);

  useEffect(() => {
    chrome.storage.local.get("post_id",(result)=>{
      if (result.post_id){
        setPick(true);
      }
    });
  }, []);

  const onClickSave=()=>{
    chrome.runtime.sendMessage({ 
      message:"post-applies", 
      post_id:post_id,
      post_name:data.post_name,
      deadline_date:data.is_closed,
      loadessay:loadDragEssay
    },(response)=>{
      setData(response.data);
    });
  }

  const onClickPick=async ()=>{
    if (!pick){
      setPick(!pick);
      await chrome.storage.local.set({post_id: post_id});
    }
    else{
      setPick(!pick);
      await chrome.storage.local.remove("post_id");
    }
  }
  const onClickLoadDragEssay=async ()=>{
    if (loadDragEssay){
      setLoadDragEssay(!loadDragEssay);
    }
    else{
      await chrome.runtime.sendMessage({ message: 'load_drag_essay' },(response)=>{
        if (response.data.title){
          setLoadDragData(response.data);
          setLoadDragEssay(!loadDragEssay);
        }
        else {
          setLoadDragData(null);
        }
      });
    }
  }

  return (<div className="post-background">
    {!data.applies && (<div className="post-icon">
      <img 
        onClick={()=>onClickSave()}
        src={SaveImage} 
        className="save-icon" 
      />
      <img 
        onClick={()=>onClickLoadDragEssay()}
        src={EssayLoadImage} 
        className={loadDragEssay ? "essayload-icon-select" : "essayload-icon"} 
      />
      <img 
        onClick={()=>onClickPick()}
        src={PickImage} 
        className={pick ? "pick-icon-select" : "pick-icon"} 
      />
    </div>)}
    <div className="post">
      <div className="post_text">
        공고 : {data.post_name}
        <a href={data.post_url} 
          target="_blank" 
          rel="noopener noreferrer"
          className="post-href"
        >
          <img 
            src={HrefImage} 
            className="href-icon"
          />
        </a>
      </div>
      <div className="post_text">기업 : {data.company_name}</div>
      <div className="post_text">채용 마감 : {data.is_closed}</div>
      {data.applies && (
        <div className="post_text">지원한 공고입니다.</div>
      )}
    </div>
    {data.applies && (data.essays.length > 0 ?
      <div className="post-essay">
        <LoadEssayList essayData={data.essays}/>
      </div> : <div>자기소개서가 없습니다.</div>
    )}
    {loadDragEssay && (loadDragData ?
      <div className="post-essay">
        <LoadEssayList essayData={loadDragData}/>
      </div> : <div>드래그한 자기소개서가 없습니다.</div>
    )}
  </div>);
}

export default Post;