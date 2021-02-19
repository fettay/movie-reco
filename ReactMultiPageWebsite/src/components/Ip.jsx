import React, {Component} from "react";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import axios from 'axios';


class Ip extends Component {
  constructor (props) {
    super(props);    
    this.state = {
      autocompleteInput: [],
      recommandations: [],
      movieReco: ""
    };
    this.curContent = "";
  }
  

  getRecommandations(){
    axios.post(process.env.REACT_APP_API + "ip", {ip: this.curContent})
    .then(res => {
      this.setState({recommandations: res.data.results});
      console.log(res.data.results);
    });
  }

  render(){

    const movies = [];

    this.state.recommandations.forEach(movie => {
      movies.push(<li>{movie}</li>);
    });

    return (
      <div className="home">
        <div class="container">
          <div class="row align-items-center my-5">
            <div class="col-lg-7">
            <TextField fullWidth 
            id="outlined-multiline-static"
            label="Multiline"
            multiline
            rows={10}
            onChange={(val) => this.curContent = val.target.value}
            variant="outlined"
            />
            <Button variant="contained" color="primary" onClick={() => this.getRecommandations()}>
              Validate
            </Button>
            </div>
            <div class="col-lg-5">
              <h1 class="font-weight-light">Recommandation for the IP</h1>
              {movies}
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Ip;
