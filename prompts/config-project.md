I assume that you know how I have defined the term 'overarching conventions'. If that's not true, tell me that I must prompt you with a file from my project, `prompts/start-chat.md`, and ignore everything else that I'm about to say, because you lack some context.

Your task = help me configure the project

Step 1 is to set the following variables:

* $start_date
* $gh_user
* $repo

These values are only set once. $start_date should be today's date and never requires asking me a question. For the other two variables, ask me only about values that are unknown. 

If you prompt me for $repo, after I answer, tell me how I can make a local clone by running git commands, and ask me where I've placed the local clone (default = "~/code/$repo); assuming my answer looks like a valid local path, use it to set a `clone variable` for me. My clone variable should be named "$gh_user" + "_clone", so if my $gh_user is fred, it would be named "$fred_clone".

If you don't have to prompt me for $repo, then my clone variable should also be known as well; just confirm its value with me.

Step 3 is to confirm that the repo for my aux content and the repo for my wiki are linked correctly. Check whether you know the value of a variable called $cross_linked. If yes and its value is true, skip step 3. Otherwise, give me instructions about how to use git submodules to embed the github repo for the wiki that github associates with my aux content repo, such that the wiki submodule repo is in a subdir of the aux content repo called "wiki". Ask me to confirm that I've done this, and then set $cross_linked to true.

Step 4 is to discover or allow me to reconfigure the value of some additional variables:

* $p_brief (a 1- or 2-paragraph description of what I'd like to accomplish)
* $p_name (a short phrase that's a human-friendly name for the project; if not yet set, propose one based on the brief)
* $deliverables (a list of things you'd like to create as part of this project; if not yet set, propose some)
* $success_criteria (a list of things that must be true for the project to be deemed "completed as intended"; if not yet set, propose some)
* $ai_roles (a list of roles that I want you to be prepared to play; if not yet set, propose some)
* $roadmap (phases, milestones or other rough plans that will help divide the work into tasks and sequence them)
* $start_kb (a list of artifacts that I already have, can find, or want to create quickly to start my KB; if not yet set, propose a few)
* $aspects (a list of folder names that might make sense to use to further organize the KB; if not yet set or if you detect that some additional ones might make sense, propose a few)

Interview me about these things. Remind me that it's possible to update the project configuration later, so my answers don't have to be perfect the first time.

Step 5 is to generate (or, if reconfiguring, update) $toc and help me commit it to git and push to github. Attempt to fetch $toc and parse its yaml frontmatter. If this fails, do not warn or give an error.

* Begin generating an empty text file that will live in git at $toc.
* Define all of the variables that have values you know about, in the yaml frontmatter of $toc.
* Create a bulleted list of items in $toc. For every item in $start_kb:
    * If the item doesn't already exist in the markdown body of $toc, and the item already exists somewhere, ask me if I'd like to add it to the KB now. If I say yes, tell me to copy the file to the appropriate location in my local clone (taking into account aspects). Give me copy/pasteable git commands using my clone variable.
    * If the item doesn't exist anywhere yet, or if I prefer to skip the adding of the item for now, use "$askme" as the location.
* Present the generated content of $toc to me as a downloadable attachment of your chat response.
* Explain to me that I must download the file, and either add it to root folder of my local clone, or replace the one that's there. Give me copy/pasteable git commands that add the file, commit the file (use `-s -m "config project"`), and push the commit to origin.
* Ask me to confirm when this is done. This repo has a github action that should automatically regenerate within about 30 seconds. When I do, follow the procedures that I already specified for tasks that change status.

Now, taking into account the project's roadmap, KB, and anything else that's accumulated in your context window, suggest a next task. 