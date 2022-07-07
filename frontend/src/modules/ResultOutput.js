import React, {useEffect, useState} from "react";
import { BallTriangle } from  'react-loader-spinner'

const ResultOutput = (queriesShouldUpdate) => {
  // Solely for 1st useEffect
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);
  // Solely for 2nd useEffect
  const [errorRes, setErrorRes] = useState(null);
  const [isLoadedRes, setIsLoadedRes] = useState(false);
  const [itemsRes, setItemsRes] = useState([]);

  const requestOptions = {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  };

  useEffect(() => {
    fetch("http://localhost:8000/search/blastquery/", requestOptions)
      .then(res => {
        if (res.status >= 400) {
          throw new Error("Server error!!")
        }
        return res.json();
      })
      .then(
        (result) => {
          setIsLoaded(true);
          setItems(result);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      );
  }, [queriesShouldUpdate, itemsRes]);

  useEffect(() => {
    const fFetch = () => {
      fetch("http://localhost:8000/search/blastresult/", requestOptions)
        .then(res => {
          if (res.status >= 400) {
            throw new Error("Server error!!")
          }
          return res.json();
        })
        .then(
          (result) => {
            setIsLoadedRes(true);
            setItemsRes(result);
            console.log(result);
          },
          (error) => {
            setIsLoadedRes(true);
            setErrorRes(error);
          }
        );
    };
    fFetch();
    const interval = setInterval(() => {
      fFetch();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h1 className="text-4xl">Blast Queries Currently in Progress:</h1>
      <ul>
        {items.map(item => {
          return !item.completed ?
            <li key={item.dna_sequence + (Math.random()*30000).toString()}>
              {item.dna_sequence.length > 40 ? item.dna_sequence.substring(0, 40) + "..." : item.dna_sequence}
              <BallTriangle height="30" width="30" color='blue' ariaLabel='loading'/>
            </li>
            :
            null
        })}
      </ul>
      <h1 className="text-4xl">Completed Queries:</h1>
      <ul>
        {itemsRes.map(item => (
          <li key={item.protein_id}>
            <p className='text-xs list-text'>
              <b>✅ {item.dna_sequence.length > 40 ? item.dna_sequence.substring(0, 40) + "..." : item.dna_sequence} </b><br/>
              <u>HSP Bit Score: </u> {item.hsp_bit_score}
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              <u>Name: </u>{item.protein_id} {item.protein_name} {item.locus_tag}
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              <u>Seq Position: </u>{item.subseq_start}-{item.subseq_end}
            </p>
          </li>
        ))}
      </ul>
    </div>
  )
};

export default ResultOutput;
