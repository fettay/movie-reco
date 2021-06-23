import React, {Component} from "react";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import axios from 'axios';
import Slider from '@material-ui/core/Slider';
import Typography from '@material-ui/core/Typography';
import ToggleButton from '@material-ui/lab/ToggleButton';
import ToggleButtonGroup from '@material-ui/lab/ToggleButtonGroup';
import GenrePicker from "./GenrePicker";
import MovieRow from "./MovieRow";


class Ip extends Component {
  constructor (props) {
    super(props);
    this.genrePicker = React.createRef();
    this.state = {
      autocompleteInput: [],
      allRecommandations: [],
      movieReco: "",
      tags: [],
      currentGenres: [],
      minYear: 1950,
      minVotes: 0
    };
    this.curContent = "A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy's room.";
    this.recoType = "TfIdf";
    this.filterRecommandation = this.filterRecommandation.bind(this);
  }
  

  getAllRecommandations(){
    // axios.post(process.env.REACT_APP_API + "themes", {ip: this.curContent})
    // .then(res => {
    //   this.setState({tags: res.data.results});
    //   console.log(res.data.results);
    // });

    axios.post(process.env.REACT_APP_API + "ip/" + this.recoType, {ip: this.curContent})
    .then(res => {
      this.setState({allRecommandations: res.data.results});
      this.setState({tags: res.data.themes});
      console.log(res.data.results);
    });
  }

  hasCommonGenre(genres, currentGenres){
    if(currentGenres.length == 0)
      return true
    return genres.filter(genre => currentGenres.includes(genre)).length > 0
  }

  filterRecommandation(currentGenres){
    if (currentGenres != this.state.currentGenres)
      this.setState({currentGenres: currentGenres});
    var recos = this.state.allRecommandations.filter(movie => this.hasCommonGenre(movie.genres, currentGenres) && movie.year >= this.state.minYear && movie.votes >= this.state.minVotes);
    return recos.slice(0, 25);                                            
  }

  handleTypeChange(event, newValue){
    this.recoType = newValue;
    this.getAllRecommandations();
  }

  componentDidMount(){
    this.getAllRecommandations();
  }

  render(){

    const movies = [];

    this.filterRecommandation(this.state.currentGenres).forEach(movie => {
      movies.push(<MovieRow id={movie.id} imgUrl={movie.cover_url} title={movie.title} tagline={movie.tagline} year={movie.year}/>);
    });

    var tags = [];
    this.state.tags.forEach(tag => {
      tags.push(<span class="badge badge-pill badge-primary tags">{tag}</span>)
    });


    return (
      <div className="home">
        <div class="container">
        <div class="row align-items-center my-5">
          <div class="col-md-6">
            <TextField fullWidth 
            id="outlined-multiline-static"
            label="Multiline"
            multiline
            rows={10}
            onChange={(val) => this.curContent = val.target.value}
            variant="outlined"
            placeholder="A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy's room."
            />
            <Button className="button-validate" variant="contained" color="primary" onClick={() => this.getAllRecommandations()}>
              Recommend
            </Button>
          </div>
          <div class="col-md-6">
              <div class="col-12">
                <ToggleButtonGroup
                  value={this.recoType}
                  exclusive
                  onChange={this.handleTypeChange.bind(this)}
                  aria-label="text alignment">
                  <ToggleButton value="Mix" aria-label="tagline">
                    Mix Model
                  </ToggleButton>
                  <ToggleButton value="TfIdf" aria-label="Hel">
                    TfIdf
                  </ToggleButton>
                  <ToggleButton value="TreeDecision" aria-label="synopsis">
                    ML Model
                  </ToggleButton>
                </ToggleButtonGroup>
              </div>
              <div class="col-md-5 genre-picker">
                  <GenrePicker ref={this.genrePicker} updateFunction={this.filterRecommandation}/>
              </div>
              <div class="col-md-5">
                  <Typography id="discrete-slider" gutterBottom>
                    Min Year:
                  </Typography>
                  <Slider
                  defaultValue={1950}
                  aria-labelledby="discrete-slider"
                  valueLabelDisplay="auto"
                  onChange={(event, newValue) => this.setState({minYear: newValue})}
                  step={10}
                  marks
                  min={1950}
                  max={2020}
                  />
              </div>
              <div class="col-md-5">
                  <Typography id="discrete-slider" gutterBottom>
                    Min Votes: (In thousands)
                  </Typography>
                  <Slider
                  defaultValue={0}
                  aria-labelledby="discrete-slider"
                  valueLabelDisplay="auto"
                  getAriaValueText={x => `${x}K`}
                  onChange={(event, newValue) => this.setState({minVotes: newValue * 200})}
                  step={10}
                  marks
                  min={0}
                  max={200}
                  />
              </div>
            </div>
          </div>
          <div class="row align-items-center my-5">
            <div class="col-lg-12">
            <div class="row tags-container">
                <div class="col-md-5">
                  {tags}
                </div>
            </div>
            <div class="table-responsive">
              <table class="table table-hover">
                <tbody>
                  {movies}
                </tbody>
              </table>
            </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Ip;
