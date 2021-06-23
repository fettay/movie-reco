import React, {Component} from "react";
import { WithContext as ReactTags } from 'react-tag-input';

const allGenres = ['Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Children', 'Comedy', 'Crime',
'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Musical',
'Mystery', 'News', 'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Talk-Show',
'Thriller', 'War', 'Western']

const KeyCodes = {
    comma: 188,
    enter: 13,
};

const genreSuggestions = allGenres.map(genre => ({id: genre, text: genre}));
const delimiters = [KeyCodes.comma, KeyCodes.enter];


class GenrePicker extends Component {

    constructor(props) {
        super(props);

        this.state = {
            tags: [{id: "Animation", text: "Animation"}] ,
            suggestions: genreSuggestions
        };
        this.handleDelete = this.handleDelete.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
    }

    handleDelete(i) {
        const { tags } = this.state;
        console.log(this.state.tags.map(x => x.id));
        this.setState({
         tags: tags.filter((tag, index) => index !== i),
        }, () => this.props.updateFunction(this.state.tags.map(x => x.id)));
    }

    handleAddition(tag) {
        console.log(this.state.tags.map(x => x.id));
        this.setState(state => ({ tags: [...state.tags, tag] }),
        () => this.props.updateFunction(this.state.tags.map(x => x.id)));
    }


    render() {
        const { tags, suggestions } = this.state;
        return (
            <div>
                <ReactTags tags={tags}
                    suggestions={suggestions}
                    handleDelete={this.handleDelete}
                    handleAddition={this.handleAddition}
                    delimiters={delimiters}
                    placeholder="Enter genres"/>
            </div>
        )
    }
};

export default GenrePicker;
