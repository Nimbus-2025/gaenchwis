import React, { memo } from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';

// useStyles를 컴포넌트 외부로 이동
const useStyles = makeStyles((theme) => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'center'
  },
  textField: {
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
    width: 250,
    textAlign: 'center'
  }
}));

const Datepicker = ({ setDate, date }) => {
  const classes = useStyles();

  const handleDateChange = (e) => {
    setDate(e.target.value);
  };

  return (
    <form className={classes.container} noValidate>
      <TextField
        id="datetime-local"
        type="datetime-local"
        defaultValue={date}
        className={classes.textField}
        onChange={handleDateChange}
        InputLabelProps={{
          shrink: true
        }}
      />
    </form>
  );
};

Datepicker.propTypes = {
  setDate: PropTypes.func.isRequired,
  date: PropTypes.string.isRequired
};

// React.memo를 사용하여 불필요한 리렌더링 방지
export default memo(Datepicker);