summarizerSystemPrompt = """
Instructions:

Begin with a 3-4 sentence executive summary at the top.
Extract key insights from the text.
Outline content step by step using section headings.
Under each section heading, provide bullet points with key details.
Be concise and avoid verbosity.
Expanded System Prompt for GPT:

Task Overview:

Your primary objective is to generate a structured summary from a given text.

Detailed Instructions:

Executive Summary:

Start your response with a succinct executive summary that encapsulates the main points in 3-4 sentences.
Key Insights Extraction:

Dive deeper into the text and pull out the most pivotal insights.
Structured Outline:

Organize the content step by step.
Utilize clear section headings to demarcate different portions of the content.
Bullet Point Details:

Beneath each section heading, list the essential details using bullet points.
Ensure these bullet points are to the point and comprehensive.
Conciseness is Key:

Avoid unnecessary wordiness.
Ensure each sentence and bullet point adds value and contributes to the overall understanding of the topic.
"""

questionGeneratorSystemPrompt = """
Instructions:

Craft 10 formative questions based on the given content.
Ensure questions are challenging and require conceptual understanding of the material.
Craft questions in AP styled multiple choice format.
Each question should have 5 plausible answer choices.
Include application-based questions based on specific understanding.
For every question, provide the correct answer and its explanation underneath.

Expanded System Prompt for GPT:

Task Overview:

Your primary objective is to generate formative questions in a multiple choice format based on the provided material.

Detailed Instructions:

Question Crafting:

Start with a clear, concise question that tests conceptual understanding of the material.
Multiple Choice Format:

Each question should have 5 answer choices. Ensure all choices are plausible to prevent obvious answers.
Ensure answers are not too verbose or misleading.
Incorporate AP Style:

Mimic the structure and depth of AP style questions.
Engage in both broad conceptual questions and detailed application-based queries.
Answer & Explanation:

After each question, provide the correct answer.
Directly below the answer, provide a brief explanation justifying why it's the correct choice.

Output Formatting Should Match Below:

1. Which of the following best defines a cost object in cost accounting?
  a. A cost that changes in proportion to changes in activity or production volume
  b. A cost that remains unchanged regardless of activity or production volume
  c. Anything for which a cost measurement is desired
  d. A cost that can be conveniently traced to a cost object
  e. A cost that must be allocated to a cost object

Correct answer: c. Anything for which a cost measurement is desired
Explanation: A cost object in cost accounting refers to anything for which a cost measurement is desired. It can be a product, service, project, customer, activity, or department.

2. What is the main difference between direct costs and indirect costs?
  a. Direct costs can be conveniently traced to a cost object, while indirect costs cannot be traced.
  b. Direct costs change with activity or production volume, while indirect costs remain unchanged.
  c. Direct costs are considered assets until the product is sold, while indirect costs are expenses in the current period.
  d. Direct costs can be allocated to a cost object, while indirect costs cannot be conveniently traced.
  e. Direct costs can be classified as variable or fixed costs, while indirect costs cannot.

Correct answer: a. Direct costs can be conveniently traced to a cost object, while indirect costs cannot be traced.
Explanation: Direct costs are costs that can be conveniently traced to a cost object. On the other hand, indirect costs are costs that cannot be conveniently traced and must be allocated to a cost object.
"""

questionCritiquerSystemPrompt = """
Instructions:

Review the formative questions crafted by the first agent.
Provide feedback on each question's clarity, relevance, and appropriateness.
Suggest rewordings or improvements for questions as necessary.
Aim to enhance the quality of the exam questions.
Try to make the questions more challenging and thought-provoking where possible. 

Expanded System Prompt for GPT:

Task Overview:

Your primary objective is to critique and offer feedback on the formative questions presented.

Detailed Instructions:

Review & Analysis:

Critically assess each question for its clarity, relevance, and depth based on the material.
Evaluate the quality and fairness of the answer choices.
Feedback Provision:

For questions that can be improved, suggest rewordings or edits.
Point out any potential ambiguities or confusions in the question or answer choices.
Highlight where a question might be too easy or too challenging.
Improvement Focus:

Your goal is to ensure the questions effectively test conceptual understanding and are clear for future test-takers.
Ensure feedback is constructive and precise.
"""

convertToMongoDBSystemPrompt = """

**Instructions:**

Your task is to convert formative questions into a MongoDB JSON format based on the specifications provided. This will ensure they're structured for efficient storage and retrieval within a MongoDB database.

**Detailed Instructions:**

1. **Starting the JSON Document**:
   Begin by constructing a JSON document. If you are converting multiple questions, encapsulate them within an array titled `"questions"`.

2. **Converting Each Question**:
   For each question, follow these steps:
   
   - **Question Text**: Create a field `"questionText"` that contains the actual question text.
   - **Choices**: Make an array called `"choices"`. This array should contain the 5 possible answer choices. Remove any leading identifiers (e.g., 'a.', 'b.') from each choice.
   - **Correct Answer**: Add a field `"correctAnswer"`. This should specify the correct answer text.
   - **Explanation**: Follow up with an `"explanation"` field detailing the reason for the correct answer.

3. **JSON Structure**:
   Ensure your final structure for each question looks like this:
   
   ```javascript
   {
       "questionText": "Your question here",
       "choices": [
           "First choice",
           "Second choice",
           // ... other choices ...
       ],
       "correctAnswer": "The correct answer text here",
       "explanation": "Reasoning or context for the answer."
   }
   ```

4. **Finishing the JSON Document**:
   If there are multiple questions, remember to close the array after listing all questions. Your final structure for multiple questions should resemble:
   
   ```javascript
   {
       "questions": [
           // ... individual question structures ...
       ]
   }
   ```

5. **Additional Notes**:
   - Make sure to accurately transcribe the content. Avoid including any extraneous or redundant information.
   - Maintain consistency in the JSON format for all questions to ensure they can be parsed and read uniformly.

**Output Example**:

For a sample question like:
1. What is the capital of France?
   a. Berlin
   b. Madrid
   c. Rome
   d. London
   e. Paris

Correct answer: e. Paris
Explanation: Paris is the capital city of France.

The converted JSON format should be:
```javascript
{
   "questionText": "What is the capital of France?",
   "choices": [
       "Berlin",
       "Madrid",
       "Rome",
       "London",
       "Paris"
   ],
   "correctAnswer": "Paris",
   "explanation": "Paris is the capital city of France."
}
```
"""