import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

const initialState = {
  fullSchedule: [],
  thisMonthSchedule: [],
  thisMonth: [],
  isOpenEditPopup: false,
  isOpenAddPopup: false,
  currentSchedule: null,
  isFilter: false
};

// API 함수
const createScheduleAPI = (scheduleData) => {
  const response = fetch('http://localhost:8000/api/v1/schedules', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(scheduleData)
  });
  return response.json();
};

// Thunk 액션 생성
export const createScheduleAsync = createAsyncThunk(
  'schedule/createScheduleAsync',
  (scheduleData) => {
    const response = createScheduleAPI(scheduleData);
    return response;
  }
);

const scheduleSlice = createSlice({
  name: 'schedule',
  initialState,
  reducers: {
    readSchedule: (state, action) => {
      const { startDay, endDay } = action.payload;
      state.thisMonthSchedule = state.fullSchedule.filter(
        schedule => schedule.date >= startDay && schedule.date <= endDay
      );
      if (state.isFilter) {
        state.thisMonth = state.thisMonthSchedule.filter(sc => sc.completed);
      } else {
        state.thisMonth = state.thisMonthSchedule;
      }
    },
    createSchedule: (state, action) => {
      const newSchedule = {
        ...action.payload,
        id: Date.now().toString(),
        completed: false
      };
      state.fullSchedule.push(newSchedule);
      state.thisMonthSchedule.push(newSchedule);
      if (!state.isFilter) {
        state.thisMonth.push(newSchedule);
      }
    },
    updateSchedule: (state, action) => {
      const updatedSchedule = action.payload;
      const updateInList = (list) => {
        const idx = list.findIndex(sc => sc.id === updatedSchedule.id);
        if (idx !== -1) list[idx] = updatedSchedule;
      };
      updateInList(state.fullSchedule);
      updateInList(state.thisMonthSchedule);
      if (!state.isFilter || updatedSchedule.completed) {
        updateInList(state.thisMonth);
      }
    },
    deleteSchedule: (state, action) => {
      const id = action.payload;
      state.fullSchedule = state.fullSchedule.filter(sc => sc.id !== id);
      state.thisMonthSchedule = state.thisMonthSchedule.filter(sc => sc.id !== id);
      state.thisMonth = state.thisMonth.filter(sc => sc.id !== id);
    },
    openEditPopup: (state, action) => {
      state.isOpenEditPopup = action.payload.isOpen;
      state.currentSchedule = action.payload.schedule || null;
    },
    setIsFilter: (state, action) => {
      state.isFilter = action.payload;
      if (action.payload) {
        state.thisMonth = state.thisMonthSchedule.filter(sc => sc.completed);
      } else {
        state.thisMonth = state.thisMonthSchedule;
      }
    },
    openAddSchedule: (state) => {
      state.isOpenAddPopup = true;
    },
    closeAddSchedule: (state) => {
      state.isOpenAddPopup = false;
    }
  },
  extraReducers: (builder) => {
    builder.addCase(createScheduleAsync.fulfilled, (state, action) => {
      const newSchedule = {
        ...action.payload,
        id: action.payload.schedule_id,
        completed: false
      };
      state.fullSchedule.push(newSchedule);
      state.thisMonthSchedule.push(newSchedule);
      if (!state.isFilter) {
        state.thisMonth.push(newSchedule);
      }
    });
  }
});

export const {
  readSchedule,
  createSchedule,
  updateSchedule,
  deleteSchedule,
  openEditPopup,
  setIsFilter,
  openAddSchedule,
  closeAddSchedule
} = scheduleSlice.actions;

export default scheduleSlice.reducer;