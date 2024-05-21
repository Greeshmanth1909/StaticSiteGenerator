# StaticSiteGenerator

A Static Site Generator converts text from a markdown file to a html file that can be presented on a website. It achieves this by parsing the given markdown and converting it into 
corresponding html block. For example, a block containing an un-ordered list like the one shown

```
* item 1
* item 2
* item 3
```

Would be converted to its corresponding html block ie `<ul>`

```
<ul>
<li>item 1</li>
<li>item 2</li>
<li>item 3</li>
</ul>
```

### Requirements
- Python 3.12.x or higher
  
### Installation
- Clone this repository with `git clone https://github.com/Greeshmanth1909/StaticSiteGenerator`
- The project doesn't require any external dependencies

## Usage

- Once the repo is cloned, run `./main.sh`. This should create a `public` directory in the root directory and start a local server that serves html generated from `.md` files in the `contents` directory
- The contents in the `public` directory can be directly hosted
- The markdown files can be linked to one another
- Static content like images should live in the `static` directory. Once `./main` is run the program copies all contents from `static` to `public` along with html generation from `contents`. Hence, static content should be referenced as how they would be stored in `public`
- The base template for html is 'template.html'



