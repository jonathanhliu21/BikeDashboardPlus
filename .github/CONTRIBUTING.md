# Contributing

Thank you for having an interest in contributing to my project. However, as I have a very busy schedule, I may not get to all of your contributions, but I will try my best. 

Before reading the rest, please read the [code of conduct](CODE_OF_CONDUCT.md). 

## Reporting bugs and issues

If you have noticed a bug in the code or your Bike Dashboard:  

- First, see if it has anything to do with the hardware
    - Did you wire something wrong?
    - Are all pins connected correctly?
    - **Note that I cannot change anything to do with the case or the mount because those are different depending on the bike**
- Try to recreate your issue and take a picture or video of it
- Look if your issue is already there in the open issues
    - If it is, then react with 👍
    - If there isn't a video already, reply to the issue with your own picture/video
    - After this, skip all other steps
- If no open issues are describing your issue, then:  
    1. Open a bug report issue (**Please use the templates provided**)
        - **Make sure the title is specific to the bug**
    2. Label the issue with the "bug" tag
    3. Describe the bug (what is happening)
    4. Describe how the bug was caused
        - Which mode you were in (bike or server)
        - Steps you made to produce the bug
    5. If any, the error message in errors.txt **at the time your issue was caused**
    6. What you expected to see vs what you actually saw
    7. A link to the picture or video showing the issue occurring
    8. Additional context: anything else you think is important to help me understand the issue
- If you think you have a solution for this problem, go to "Pull Requests"

If I find out that this bug is actually happening, then I will add it to the list of "Problems that still occur" in the README. 

## Suggestions/feedback/questions

- First check:  
    1. Does this have anything to do with hardware (the case/mount)?
        - If yes, I cannot work on it because it is different depending on the bike.
    2. Does this have anything to do with electronics (wiring)?
        - I may be able to work on the wiring of the different components, but this will be rare.
    3. If an enhancement, will it be a major change, and will it be very time-consuming?
        - If yes, I may put this as a feature in the next major version of Bike Dashboard. 
    4. Is your suggestion in the list of open issues already? 
        - If yes, react to that issue with 👍 and ignore all other steps

If the answers to the above questions are "No", classify your issue and then open an issue:
**Make sure the title is specific to your suggestion/feedback/question**

- Upgrade idea:
    - Label with "enhancement"
    - Name the feature you want to enhance and why you want to enhance it (are you annoyed/frustrated by something in the feature?) OR name a feature you want to add and why you want to add it
    - Explain how you want to enhance it or want it to be enhanced OR explain about your proposed feature
    - Include links to photos, videos, diagrams, etc if necessary
    - If you think you want to write the code yourself, see "Pull requests"
- Questions
    - Label with "question"
    - Describe the type of question:
        - Clarification
        - Question about a feature (what it does, how it works, etc.)
        - Questions about the project itself (how I made it, etc.)
        - Other question
    - Ask the question
- Documentation feedback
    - Label with "documentation"
    - Name the file
    - Quote the part of the file that seems wrong and describe what is wrong
- Other feedback
    - Label with "feedback"
    - Describe the feedback

If I approve of the enhancement, I will add it to "Upgrade ideas" in README.

## Pull Requests

Note that code reviewing will be very slow due to my busy schedule. I will review most of the bug fixes first before moving on to the enhancements. 

1. Fork the repository
2. Create a new branch in your forked repository that you will fix a bug on or enhance/add a feature on
3. Work on your code and create a pull request to the **develop** branch of the base repository (**Please use the template provided**)
4. Make changes to the docs if necessary
5. Wait for review

In the pull request, include:
- A **specific** title
- A link to the corresponding issue
- Summary of what you've changed
- How you tested the change
- Any new dependencies required

**Important**  
Before you submit, make sure you have:
- Self-reviewed your code
- Commented your code so it is easy to read and follow
- Tested to make sure your code works or your fix is effective
- Made corresponding changes to the docs
- Read this checklist
