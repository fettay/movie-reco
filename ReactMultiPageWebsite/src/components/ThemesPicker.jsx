import React, {Component} from "react";
import { WithContext as ReactTags } from 'react-tag-input';
import allThemes from "../allThemes";


const KeyCodes = {
    comma: 188,
    enter: 13,
};

const themeSuggestions = allThemes.map(theme => ({id: theme, text: theme}));
const delimiters = [KeyCodes.comma, KeyCodes.enter];


class ThemesPicker extends Component {

    constructor(props) {
        super(props);

        this.state = {
            tags: [] ,
            suggestions: themeSuggestions
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

    handleAdditionClick(e) {
        var tag = e.target.getAttribute("value")
        tag = {id: tag, text: tag};
        this.handleAddition(tag);
    }

    handleAddition(tag) {
        this.setState(state => ({ tags: [...state.tags, tag] }),
        () => this.props.updateFunction(this.state.tags.map(x => x.id)));
    }


    render() {
        const { tags, suggestions } = this.state;

        var recommendedTags = [];
        this.props.recommendedTags.forEach(tag => {
            recommendedTags.push(<span class="badge badge-primary tags" value={tag} onClick={(e) => this.handleAdditionClick(e)}>{tag}</span>)
        });
        return (
            <div>
                <div>
                    <ReactTags tags={tags}
                        suggestions={suggestions}
                        handleDelete={this.handleDelete}
                        handleAddition={this.handleAddition}
                        delimiters={delimiters}
                        placeholder="Themes for filtering"/>
                </div>
                <div class="row tags-container">
                    <div class="col-md-12">
                        {recommendedTags}
                    </div>
                </div>
            </div>
        )
    }
};

export default ThemesPicker;

