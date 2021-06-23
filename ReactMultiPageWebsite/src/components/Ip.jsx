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


const allThemes = ["abortion", "accident", "africanamerican", "afterlife", "againsttherules", "agedifference", "agent", "aging", "airdisaster", "airplane", "airport", "alcohol", "alien", "alternatereality", "ambition", "angel", "anger", "animal", "apocalypse", "archaeologist", "army", "arrangedmarriage", "arrest", "art", "artist", "assassination", "astronaut", "attack", "audition", "baby", "ballet", "bandit", "bar", "baseball", "basketball", "battle", "beach", "beast", "beating", "bestfriend", "bet", "betrayal", "bird", "birthday", "bisexual", "blackmail", "blood", "boat", "bodyguard", "bollywood", "bomb", "bondage", "bountyhunter", "boxing", "breakup", "brother", "business", "camp", "campaign", "cannibalism", "car", "career", "castle", "cat", "cave", "cellphone", "cemetery", "championship", "chaos", "chase", "cheating", "chess", "child", "christmas", "church", "city", "civilwar", "clown", "cocaine", "coldwar", "coma", "communism", "competition", "computer", "concert", "confession", "cooking", "corruption", "couple", "courage", "cowboy", "crime", "criminal", "curse", "custody", "dance", "danger", "dating", "death", "debt", "deception", "depression", "desert", "desire", "desperation", "destiny", "destruction", "devil", "diary", "diner", "disability", "disappearance", "disguise", "dishonesty", "disorder", "distopia", "doctor", "dog", "doll", "domesticviolence", "downfall", "dragon", "dream", "drowning", "drug", "earthquake", "elevator", "escape", "experiment", "exploitation", "factory", "faith", "fallinlove", "falseaccusation", "fame", "family", "farm", "fascism", "fashion", "father", "fear", "fight", "fire", "firstlove", "fish", "football", "forbiddenlove", "forest", "freedom", "friend", "gambling", "game", "gangster", "gender", "generationgap", "gettinghome", "ghetto", "ghost", "giant", "god", "gold", "goodversusevil", "governmentagency", "grief", "guilt", "hacker", "halloween", "hallucination", "hanging", "hauntedbythepast", "helicopter", "hero", "hiddenidentity", "highsociety", "hiphop", "hippie", "hollywood", "homeinvasion", "homeless", "homosexual", "hope", "horse", "hospital", "hostage", "hotel", "housewife", "humiliation", "hunting", "hypnosis", "illness", "imagination", "immortality", "impossiblelove", "incest", "injury", "injustice", "insanity", "intelligence", "interracialrelations", "interview", "invasion", "inventionsanddiscoveries", "investigation", "island", "isolation", "jazz", "jealousy", "jewish", "journalism", "judge", "justice", "juveniledelinquency", "kidnapping", "killer", "king", "kitchen", "knight", "lake", "lawyer", "leadership", "legendsandmyths", "lie", "lifestylechange", "loneliness", "lossofvirginity", "love", "loveinterest", "loyalty", "lust", "machismo", "mafia", "magic", "manhunt", "manipulation", "martialarts", "massacre", "masterandservant", "masturbation", "medieval", "medium", "memory", "mentalillness", "mentalinstitution", "mentor", "military", "mindcontrol", "mindgame", "miracle", "mirror", "misfit", "mission", "mistakenidentity", "mistress", "money", "monkey", "monster", "moon", "moraldilemma", "mother", "motherdaughterrelationship", "mothersonrelationship", "motorcycle", "mountain", "murder", "murderer", "music", "muslim", "mutant", "muteordeaf", "mystery", "nanny", "nature", "nightclub", "nightmare", "ninja", "obsession", "office", "oldman", "ontheroad", "outerspace", "painting", "parallelworld", "paranoia", "parody", "party", "passion", "philosophy", "photograph", "physicalappearance", "poker", "police", "politics", "poverty", "pregnancy", "princess", "prison", "privatedetective", "profanity", "promise", "prostitute", "psychology", "punishment", "puppet", "rage", "rape", "rebellion", "redemption", "rehabilitation", "relationship", "religion", "rescue", "resistance", "restaurant", "revenge", "rivalry", "robot", "sacrifice", "salesman", "school", "science", "sea", "secret", "securityguard", "sex", "sexism", "shark", "sheriff", "ship", "showbiz", "siblingrelationship", "singlemother", "slavery", "smuggling", "snake", "sniper", "soccer", "socialdifferences", "society", "soldier", "specialagents", "spy", "stabbing", "stalking", "stereotype", "store", "storm", "strangulation", "strongfemalepresence", "suburb", "subway", "success", "suicide", "summer", "supernatural", "superpower", "surrealism", "surveillance", "survival", "suspicion", "swimming", "sword", "talkinganimals", "tattoo", "taxi", "team", "technology", "teenager", "teleportation", "terrorism", "theater", "threat", "timetravel", "torture", "tourist", "tragedy", "tragichero", "transsexual", "travel", "treason", "truck", "twin", "unemployment", "university", "unlikelyfriendships", "unlikelypartners", "vampire", "vengeance", "village", "violence", "virgin", "war", "weapon", "wedding", "widow", "wine", "winter", "witch", "womanizer", "wooing", "workplace", "worldwarone", "worldwartwo", "wrestling", "writer", "younglovers", "youngwoman", "youth", "zombie"];


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
    this.curContent = "";
    this.recoType = "TfIdf";
    this.filterRecommandation = this.filterRecommandation.bind(this);
  }
  

  updateThemes(themesBinary){
    var themes = allThemes.filter((t, i) => themesBinary[i] == 1);
    this.setState({tags: themes});
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
      this.updateThemes(res.data.themes);
      console.log(res.data.results);
    });
  }

  hasCommonGenre(genres, currentGenres){
    return genres.filter(genre => currentGenres.includes(genre)).length > 0
  }

  filterRecommandation(currentGenres){
    if (currentGenres != this.state.currentGenres)
      this.setState({currentGenres: currentGenres});
    var recos = this.state.allRecommandations.filter(movie => this.hasCommonGenre(movie.genres, currentGenres) && movie.year >= this.state.minYear && movie.votes >= this.state.minVotes);
    return recos.slice(0, 25).map(movie => movie.title);                                            
  }

  handleTypeChange(event, newValue){
    this.recoType = newValue;
    this.getAllRecommandations();
  }

  render(){

    const movies = [];

    // this.filterRecommandation(this.state.currentGenres).forEach(movie => {
    //   movies.push(<MovieRow></MovieRow>);
    // });

    Array(8).fill(0).forEach(() => {
        movies.push(<MovieRow></MovieRow>);
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
            />
            <Button variant="contained" color="primary" onClick={() => this.getAllRecommandations()}>
              Validate
            </Button>
          </div>
          <div class="col-md-6">
              <div class="col-12">
                <ToggleButtonGroup
                  value={this.recoType}
                  exclusive
                  onChange={this.handleTypeChange.bind(this)}
                  aria-label="text alignment">
                  <ToggleButton value="DL" aria-label="tagline">
                    DL Model
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
            <table class="table table-hover">
              <tbody>
                {movies}
              </tbody>
            </table>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Ip;
