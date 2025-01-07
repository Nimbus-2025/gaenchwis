import React, { memo } from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@mui/styles';
import TextField from '@mui/material/TextField';
import styled from 'styled-components';


const DateInput = styled.input`
  font-size: 1.2em;
  color: #333;
  text-align: center;
  border: none;
  background: transparent;
  cursor: pointer;
  
  &:focus {
    outline: none;
  }
`;

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

const Datepicker = ({ setDate, date, readOnly }) => {
  return (
    <DateInput
      type="datetime-local"
      value={date}
      onChange={(e) => setDate(e.target.value)}
      readOnly={readOnly}
    />
  );
};

Datepicker.propTypes = {
  setDate: PropTypes.func.isRequired,
  date: PropTypes.string.isRequired
};

// React.memo를 사용하여 불필요한 리렌더링 방지
export default memo(Datepicker);


