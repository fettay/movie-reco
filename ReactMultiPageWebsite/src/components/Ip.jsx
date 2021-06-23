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
import ThemesPicker from "./ThemesPicker";
import DotLoader from "react-spinners/DotLoader";


const default_ip = "A little boy named Andy loves to be in his room, playing with his toys, especially his doll named Woody. But, what do the toys do when Andy is not with them, they come to life. Woody believes that his life (as a toy) is good. However, he must worry about Andy\'s family moving, and what Woody does not know is about Andy\'s birthday party. Woody does not realize that Andy\'s mother gave him an action figure known as Buzz Lightyear, who does not believe that he is a toy, and quickly becomes Andy\'s new favorite toy. Woody, who is now consumed with jealousy, tries to get rid of Buzz. Then, both Woody and Buzz are now lost. They must find a way to get back to Andy before he moves without them, but they will have to pass through a ruthless toy killer";

const override = `
  display: block;
  margin: 0 auto;
`;

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
      currentThemes: [],
      minYear: 1950,
      minVotes: 0
    };
    this.isLoading = false;
    this.curContent = default_ip
    this.recoType = "TfIdf";
    this.filterRecommandation = this.filterRecommandation.bind(this);
    this.handleThemeAdd = this.handleThemeAdd.bind(this);
    this.handleGenreAdd = this.handleGenreAdd.bind(this);
  }
  

  getAllRecommandations(){
    // axios.post(process.env.REACT_APP_API + "themes", {ip: this.curContent})
    // .then(res => {
    //   this.setState({tags: res.data.results});
    //   console.log(res.data.results);
    // });

    this.isLoading = true;

    axios.post(process.env.REACT_APP_API + "ip/" + this.recoType, {ip: this.curContent})
    .then(res => {
      this.setState({allRecommandations: res.data.results});
      this.setState({tags: res.data.themes});
      this.isLoading = false;;
    });
  }

  hasCommonGenre(genres, currentGenres){
    if(currentGenres.length == 0)
      return true
    return genres.filter(genre => currentGenres.includes(genre)).length > 0
  }

  hasAllThemes(themes, currentThemes){
    if(currentThemes.length == 0)
      return true
    return currentThemes.filter(theme => themes.includes(theme)).length == currentThemes.length;
  }

  handleThemeAdd(currentThemes){
    this.setState({currentThemes: currentThemes});
  }

  handleGenreAdd(currentGenres){
    this.setState({currentGenres: currentGenres});
  }

  filterRecommandation(){
    var recos = this.state.allRecommandations.filter(movie => this.hasCommonGenre(movie.genres, this.state.currentGenres) && movie.year >= this.state.minYear && movie.votes >= this.state.minVotes && this.hasAllThemes(movie.themes, this.state.currentThemes));
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

    this.filterRecommandation(this.state.currentGenres, this.state.currentThemes).forEach(movie => {
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
            placeholder={default_ip}
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
                  <GenrePicker ref={this.genrePicker} updateFunction={this.handleGenreAdd}/>
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
            <ThemesPicker recommendedTags={this.state.tags} updateFunction={this.handleThemeAdd} />
            <DotLoader color="#3f51b5" loading={!this.isLoading} css={override} size={70} />
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
