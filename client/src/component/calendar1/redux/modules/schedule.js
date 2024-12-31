import { createReducer, createAction } from '@reduxjs/toolkit';
import { db } from '../../../calendar1/Firebase';
import { collection, addDoc, getDocs, updateDoc, deleteDoc, doc } from 'firebase/firestore';
import { makeStyles } from '@mui/styles';
export const OPEN_ADD_SCHEDULE = 'schedule/OPEN_ADD_SCHEDULE';
export const CLOSE_ADD_SCHEDULE = 'schedule/CLOSE_ADD_SCHEDULE';

// `schedule` 컬렉션 정의
const scheduleCollection = collection(db, 'schedule');

// Constants
const COLLECTION_NAME = 'schedule';

// Initial State
export const initialState = {
  fullSchedule: [],
  thisMonthSchedule: [],
  thisMonth: [],
  isOpenEditPopup: false,
  currentSchedule: null,
  isFilter: false,
  isOpenAddPopup: false
};

// Action Creators
export const fetchFullSchedule = createAction('schedule/FETCH_FULL_SCHEDULE');
export const addSchedule = createAction('schedule/ADD_SCHEDULE');
export const editSchedule = createAction('schedule/EDIT_SCHEDULE');
export const removeSchedule = createAction('schedule/REMOVE_SCHEDULE');
export const filterThisMonth = createAction('schedule/FILTER_THIS_MONTH');
export const openEditPopup = createAction('schedule/OPEN_EDIT_POPUP');
export const setCurrentSchedule = createAction('schedule/SET_CURRENT_SCHEDULE');
export const setIsFilter = createAction('schedule/SET_IS_FILTER');

// Reducer
const schedule = createReducer(initialState, {
  [fetchFullSchedule]: (state, { payload }) => {
    state.fullSchedule = payload.fullList;
    state.thisMonthSchedule = payload.thisMonthSchedule;
    state.thisMonth = state.isFilter 
      ? state.thisMonthSchedule.filter(sc => sc.completed) 
      : state.thisMonthSchedule;
  },

  [openEditPopup]: (state, { payload: { isOpen, schedule } }) => {
    state.isOpenEditPopup = isOpen;
    state.currentSchedule = schedule;
  },

  [setIsFilter]: (state, { payload }) => {
    state.isFilter = payload;
  },

  [addSchedule]: (state, { payload }) => {
    state.fullSchedule = [...state.fullSchedule, payload];
  },

  [editSchedule]: (state, { payload }) => {
    const updateSchedule = (list) => 
      list.map(item => item.id === payload.id ? payload : item);

    state.fullSchedule = updateSchedule(state.fullSchedule);
    state.thisMonth = updateSchedule(state.thisMonth);
    state.currentSchedule = payload;
  },

  [removeSchedule]: (state, { payload }) => {
    const filterSchedule = (list) => 
      list.filter(item => item.id !== payload);

    state.fullSchedule = filterSchedule(state.fullSchedule);
    state.thisMonth = filterSchedule(state.thisMonth);
    state.currentSchedule = null;
  },

  [filterThisMonth]: (state, { payload: { startDay, endDay } }) => {
    state.thisMonth = state.fullSchedule.filter(sc => {
      const dateInRange = 
        parseInt(sc.date) >= parseInt(startDay) &&
        parseInt(sc.date) <= parseInt(endDay);
      
      return state.isFilter ? dateInRange && sc.completed : dateInRange;
    });
  },

  [OPEN_ADD_SCHEDULE]: (state) => {
    return {
      ...state,
      isOpenAddPopup: true
    };
  },

  [CLOSE_ADD_SCHEDULE]: (state) => {
    return {
      ...state,
      isOpenAddPopup: false
    };
  }
});

// Thunks
export const createSchedule = (data) => async (dispatch) => {
  try {
    const saveData = { ...data, completed: false };
    const docRef = await db.add(saveData);
    const schedule = { ...saveData, id: docRef.id };
    dispatch(addSchedule(schedule));
  } catch (error) {
    console.error('Error creating schedule:', error);
    // 에러 처리 로직 추가
  }
};

export const readSchedule = ({ startDay, endDay }) => async (dispatch) => {
  try {
    const snapshot = await db.get();
    const fullList = snapshot.docs
      .filter(doc => doc.exists)
      .map(doc => ({ ...doc.data(), id: doc.id }));

    const thisMonthSchedule = fullList.filter(sc => 
      parseInt(sc.date) >= parseInt(startDay) &&
      parseInt(sc.date) <= parseInt(endDay)
    );

    dispatch(fetchFullSchedule({ fullList, thisMonthSchedule }));
  } catch (error) {
    console.error('Error reading schedule:', error);
    // 에러 처리 로직 추가
  }
};

export const updateSchedule = (data) => async (dispatch) => {
  try {
    await updateDoc(doc(scheduleCollection, data.id), data);
    dispatch(editSchedule(data));
  } catch (error) {
    console.error('Error updating schedule:', error);
    // 에러 처리 로직 추가
  }
};

export const deleteSchedule = (id) => async (dispatch) => {
  try {
    await deleteDoc(doc(scheduleCollection, id));
    dispatch(removeSchedule(id));
  } catch (error) {
    console.error('Error deleting schedule:', error);
    // 에러 처리 로직 추가
  }
};

export const openAddSchedule = () => ({
  type: OPEN_ADD_SCHEDULE,
});

export const closeAddSchedule = () => ({
  type: CLOSE_ADD_SCHEDULE,
});

export default schedule; 