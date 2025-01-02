import { createReducer, createAction } from '@reduxjs/toolkit';
import moment from 'moment';
import { db } from '../../../calendar1/Firebase';
import { collection, addDoc, getDocs, updateDoc, deleteDoc, doc } from 'firebase/firestore';

// ... 나머지 코드

// Constants
const COLLECTION_NAME = 'schedule';
const scheduleCollection = collection(db, 'schedule');

// Action Types
export const OPEN_ADD_SCHEDULE = 'schedule/OPEN_ADD_SCHEDULE';
export const CLOSE_ADD_SCHEDULE = 'schedule/CLOSE_ADD_SCHEDULE';
export const TOGGLE_SCHEDULE_VISIBILITY = 'schedule/TOGGLE_SCHEDULE_VISIBILITY';

// Initial State
export const initialState = {
  fullSchedule: [],
  thisMonthSchedule: [],
  thisMonth: [],
  isOpenEditPopup: false,
  currentSchedule: null,
  isFilter: false,
  isOpenAddPopup: false,
  isVisible: true
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
export const toggleScheduleVisibility = createAction('schedule/TOGGLE_SCHEDULE_VISIBILITY');

// Reducer
const schedule = createReducer(initialState, {
  [fetchFullSchedule]: (state, action) => {
    state.fullSchedule = action.payload.fullList;
    state.thisMonthSchedule = action.payload.thisMonthSchedule;
    state.thisMonth = state.isFilter 
      ? state.thisMonthSchedule.filter(sc => sc.completed) 
      : state.thisMonthSchedule;
  },

  [openEditPopup]: (state, action) => {
    if (typeof action.payload === 'boolean') {
      state.isOpenEditPopup = action.payload;
    } else {
      state.isOpenEditPopup = action.payload.isOpen;
      state.currentSchedule = action.payload.schedule;
    }
  },

  [setIsFilter]: (state, action) => {
    state.isFilter = action.payload;
  },

  [addSchedule]: (state, action) => {
    state.fullSchedule = [...state.fullSchedule, action.payload];
    const currentDate = new Date();
    const scheduleDate = new Date(
      action.payload.date.substring(0, 4),
      parseInt(action.payload.date.substring(4, 6)) - 1,
      action.payload.date.substring(6)
    );
    if (
      currentDate.getFullYear() === scheduleDate.getFullYear() &&
      currentDate.getMonth() === scheduleDate.getMonth()
    ) {
      state.thisMonth = [...state.thisMonth, action.payload];
    }
  },

  [editSchedule]: (state, action) => {
    const updateSchedule = (list) => 
      list.map(item => item.id === action.payload.id ? action.payload : item);

    state.fullSchedule = updateSchedule(state.fullSchedule);
    state.thisMonth = updateSchedule(state.thisMonth);
    state.currentSchedule = action.payload;
  },

  [removeSchedule]: (state, action) => {
    const filterSchedule = (list) => 
      list.filter(item => item.id !== action.payload);

    state.fullSchedule = filterSchedule(state.fullSchedule);
    state.thisMonth = filterSchedule(state.thisMonth);
    state.currentSchedule = null;
  },

  [filterThisMonth]: (state, action) => {
    state.thisMonth = state.fullSchedule.filter(sc => {
      const dateInRange = 
        parseInt(sc.date) >= parseInt(action.payload.startDay) &&
        parseInt(sc.date) <= parseInt(action.payload.endDay);
      
      return state.isFilter ? dateInRange && sc.completed : dateInRange;
    });
  },

  [OPEN_ADD_SCHEDULE]: (state) => {
    state.isOpenAddPopup = true;
  },

  [CLOSE_ADD_SCHEDULE]: (state) => {
    state.isOpenAddPopup = false;
  },

  [toggleScheduleVisibility]: (state) => {
    state.isVisible = !state.isVisible;
  }
});

// Thunks
export const createSchedule = (data) => async (dispatch) => {
  try {
    console.log('Creating schedule - Received data:', data); // 디버깅 로그

    // Firestore에 저장할 데이터 준비
    const saveData = {
      ...data,
      completed: false,
      date: data.date.toString(),
      time: data.time.toString(),
      createdAt: new Date().toISOString()
    };

    console.log('Saving to Firestore:', saveData); // 디버깅 로그

    // Firestore에 저장
    const docRef = await addDoc(scheduleCollection, saveData);
    console.log('Document written with ID:', docRef.id); // 디버깅 로그

    // Redux store 업데이트
    const schedule = { ...saveData, id: docRef.id };
    dispatch(addSchedule(schedule));

    return { success: true, id: docRef.id };
  } catch (error) {
    console.error('Error in createSchedule:', error);
    throw error;
  }
};

export const readSchedule = ({ startDay, endDay }) => async (dispatch) => {
  try {
    console.log('Reading schedules for:', { startDay, endDay });
    const snapshot = await getDocs(scheduleCollection);
    const fullList = snapshot.docs
      .filter(doc => doc.exists())
      .map(doc => ({ ...doc.data(), id: doc.id }));

    const thisMonthSchedule = fullList.filter(sc => 
      parseInt(sc.date) >= parseInt(startDay) &&
      parseInt(sc.date) <= parseInt(endDay)
    );

    console.log('Fetched schedules:', { fullList, thisMonthSchedule });
    dispatch(fetchFullSchedule({ fullList, thisMonthSchedule }));
  } catch (error) {
    console.error('Error reading schedule:', error);
  }
};

export const updateSchedule = (data) => async (dispatch) => {
  try {
    console.log('Updating schedule:', data);
    await updateDoc(doc(scheduleCollection, data.id), data);
    dispatch(editSchedule(data));
  } catch (error) {
    console.error('Error updating schedule:', error);
  }
};

export const deleteSchedule = (id) => async (dispatch) => {
  try {
    console.log('Deleting schedule:', id);
    await deleteDoc(doc(scheduleCollection, id));
    dispatch(removeSchedule(id));
  } catch (error) {
    console.error('Error deleting schedule:', error);
  }
};

export const openAddSchedule = () => ({
  type: OPEN_ADD_SCHEDULE,
});

export const closeAddSchedule = () => ({
  type: CLOSE_ADD_SCHEDULE,
});

export default schedule;