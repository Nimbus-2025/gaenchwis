import { configureStore } from '@reduxjs/toolkit';
import schedule from './modules/schedule';

const store = configureStore({
  reducer: {
    schedule: schedule
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['schedule/FETCH_FULL_SCHEDULE'],
        ignoredPaths: ['schedule.fullSchedule', 'schedule.thisMonthSchedule']
      }
    }),
  devTools: process.env.NODE_ENV !== 'production'
});

export { store };