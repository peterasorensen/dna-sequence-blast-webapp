import {Form, FormikProvider, useFormik} from "formik";
import * as Yup from "yup";
import React, {useState} from "react";
import TextInputLiveFeedback from "../components/Input/TextInputLiveFeedback";
import Cookies from 'js-cookie';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const DNASeqForm = ({queriesShouldUpdate, setQueriesShouldUpdate}) => {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [postSuccess, setPostSuccess] = useState(false);

  const clearStatus = () => {
    setPostSuccess(false);
    setIsLoaded(false);
    setError(false);
  };

  const formik = useFormik({
    initialValues: {
      dna_seq: '',
    },
    onSubmit: async (values) => {
      clearStatus();
      await sleep(500);
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          "user_cookie": Cookies.get('user_cookie'),
          "dna_sequence": values.dna_seq,
          "title": "-",
          "description": "-",
          "completed": false
        })
      };
      fetch('http://localhost:8000/search/blastquery/', requestOptions)
        .then(res => {
          if (res.status >= 400) {
            throw new Error("Server error!!")
          }
          return res.json();
        })
        .then(
          (result) => {
            setIsLoaded(true);
            setPostSuccess(true);
          },
          (error) => {
            setIsLoaded(true);
            setError(error);
          }
        );
      await sleep(100);
      // make this change to trigger useEffect in ResultOutput Loading Component
      setQueriesShouldUpdate(!queriesShouldUpdate);
    },
    onReset: async () => {
      clearStatus();
    },
    validationSchema: Yup.object({
      dna_seq: Yup.string()
        .min(3, 'Must be at least 8 characters')
        // .max(270, 'Must be less  than 270 characters')
        .required('A DNA sequence is required')
        .matches(
          /^[actgACTG]+$/,
          'Must be nucleic acid notation (ATCG only).'
        ),
    }),
  });

  return (
    <FormikProvider value={formik}>
      <Form>
        <TextInputLiveFeedback
          label="DNA Sequence"
          id="dna_seq"
          name="dna_seq"
          helpText="Must be at least 3 characters, no spaces and only contain nucleic acid notation (ATCG)."
          type="text"
        />
        <div>
          <button type="submit">Submit</button>
          <button type="reset">Reset</button>
          {postSuccess ? <p className="text-submitted">Submitted ✓</p> : null}
          {error ? <p className="submission-error">Server Error! ✗ {error.toString()}</p> : null}
        </div>
      </Form>
    </FormikProvider>
  );
};

export default DNASeqForm;
