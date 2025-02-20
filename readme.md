An SFT model trained from the base model facebook-Bart-base intended to take in tasks described in natural language and generate Solidity code snippets that implement them.

The task is considered to be text generation task. In which the model is expected to interpret natural lnaguage tasks and generate functions that carry them out.

We get the base model using the transformer library provided by hugging face.

**Setup**

Create a file called `private_info.py` and copy n paste the following.
To learn more about `gh_access_token` and how to obtain it, [click here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

```
gh_access_token = # ADD YOUR gh_access_token here
```

Python dependencies could be found in `dependencies.txt`

Use the following command to install python dependencies
```
pip install -r dependencies.txt
```