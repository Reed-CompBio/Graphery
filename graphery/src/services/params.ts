export const emptyTutorialContentTag = '<None>';

export const newModelUUID = '00000000-0000-0000-0000-000000000000';

// TODO pull data from i18n
export const langList = ['en-us', 'zh-cn'];

export const emptyCodeTemplate = `# python 3.8 Empty Code Template
from bundle.seeker import tracer
from bundle.utils.dummy_graph import graph_object


# put the name of the variables (as string) you want to trace 
# in the tracer decorator 
@tracer('greeting')
def main() -> None:
    greeting: str = 'hello world :)'
    print(greeting)

# For more info please checkout 
# https://github.com/FlickerSoul/Graphery/tree/master/backend/bundle#readme
`;

export const localServerTargetVersion = '0.1.0';
