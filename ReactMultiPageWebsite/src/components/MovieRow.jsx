import React, {Component} from "react";


class MovieRow extends Component {

    constructor(props){
        super(props);
    }

    render() {
        return (
        <tr class="movie-row clickable-row" onClick={() => window.open("https://www.imdb.com/title/tt" + this.props.id, "_blank")}>
            <td class='movie-row-img'>
                <img class="img-fluid" src={this.props.imgUrl} alt={this.props.name}/>
            </td>
            <td>
                <h5>{this.props.title} 
                    <em>({this.props.year})</em>
                </h5> 
                <br/>
                {this.props.tagline}
            </td>
        </tr>
        )};
}

export default MovieRow;