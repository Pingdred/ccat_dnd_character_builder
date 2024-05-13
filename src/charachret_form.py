import json

from langchain.chains import LLMChain
from langchain_core.runnables import RunnableConfig
from cat.looking_glass.callbacks import NewTokenHandler
from langchain_core.prompts.prompt import PromptTemplate

from cat.utils import get_static_path
from cat.looking_glass.prompts import MAIN_PROMPT_PREFIX

from cat.experimental.form import form, CatForm, CatFormState
from .character_sheet import CharacterSheet

@form
class DnDCharacter(CatForm):
    model_class = CharacterSheet
    description = "Create a new character for the game Dungeon and Dragons."
    ask_confirm = True
    
    start_examples =  [
        "Create a new DnD character"
    ]

    def message_incomplete(self):
        out = f"""Character Sheet:

```json
{json.dumps(self._model, indent=4)}
```
"""
        self.cat.send_ws_message(out, "chat")

        separator = "\n - "
        missing_fields = ""
        if self._missing_fields:
            missing_fields = "\nMissing fields:"
            missing_fields += separator + separator.join(self._missing_fields)
        invalid_fields = ""
        if self._errors:
            invalid_fields = "\nInvalid fields:"
            invalid_fields += separator + separator.join(self._errors)

        chat_history = self.cat.stringify_chat_history()
        prefix = self.get_prefix()
        prompt = f"""{prefix}
        
Your task is to assist in the creation of a character sheet for DnD, use the information below to assist 
the human providing useful hints, asking for the missing fields and providing information about eventual errors.

{{out}}

{missing_fields}

{invalid_fields}

{chat_history}
AI:"""

        extraction_chain = LLMChain(
            prompt     = PromptTemplate.from_template(prompt),
            llm        = self._cat._llm,
            verbose    = True,
            output_key = "output"
        )
        llm_responce = extraction_chain.invoke(input={"out":out}, config=RunnableConfig(callbacks=[NewTokenHandler(self.cat)]))["output"]

        return {
            "output": llm_responce
        }

    def message_wait_confirm(self):
        out = f"""Character Sheet:

```json
{json.dumps(self._model, indent=4)}
```
"""
        if self._state == CatFormState.WAIT_CONFIRM:
            out += "\n --> Confirm? Yes or no?"
            return {
                "output": out
            }

    def submit(self, form_data) -> str:

        static_path = get_static_path()

        file_name = form_data['name'].replace(" ", "_")

        # Directly from dictionary
        with open(f"{static_path}{file_name}.json", 'w') as outfile:
            json.dump(form_data, outfile)


        return {
            "output": "Character sheet saved"
        }
    
    def get_prefix(self):

        prefix = self.cat.mad_hatter.execute_hook(
            "agent_prompt_prefix",
            MAIN_PROMPT_PREFIX,
            cat=self.cat
        )

        return prefix
