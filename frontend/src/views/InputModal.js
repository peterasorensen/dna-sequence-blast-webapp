import DNASeqForm from "../modules/DNASeqForm";
import React from "react";

const InputModal = ({queriesShouldUpdate, setQueriesShouldUpdate}) => {
  return (
    <div className="app">
      <h1 className="text-4xl">DNA Sequence Asynchronous Alignment Search with Blast</h1>
      <p className="text-lg">
        Proteins from the following genomes are searched until one is found
        containing the provided input sequence. Note: A single genome may contain
        more than one protein. <br/>
        <i>NC_000852, NC_007346, NC_008724, NC_009899, NC_014637, NC_020104, NC_023423,
          NC_023640, NC_023719, NC_027867</i> <br/>
      </p>
      <div className="example">
        <DNASeqForm queriesShouldUpdate={queriesShouldUpdate} setQueriesShouldUpdate={setQueriesShouldUpdate}/>
      </div>
      <p className="text-md mt-1">
        <strong>Note:</strong> Each query maps to exactly one output. There may
        be more valid matches in the Blast search, but a random one is chosen
        for each query. The alignment score for each output is displayed along
        with the starting and ending positions of where the subsequence was found
        in the protein's sequence.
      </p>
      {/*<p className="text-sm">*/}
      {/*  <i>*/}
      {/*    Example adapted from{' '}*/}
      {/*    <a*/}
      {/*      href="https://www.w3.org/WAI/tutorials/forms/notifications/"*/}
      {/*      target="blank"*/}
      {/*      rel="noopener noreferrer"*/}
      {/*    >*/}
      {/*      W3C WAI Web Accessibility Tutorials*/}
      {/*    </a>*/}
      {/*  </i>*/}
      {/*</p>*/}
    </div>
  )
};

export default InputModal;
