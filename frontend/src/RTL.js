import { create } from 'jss';
import rtl from 'jss-rtl';
import { StylesProvider, jssPreset } from '@mui/styles';

const jss = create({ plugins: [...jssPreset().plugins, rtl()] });

function RTL(props) {
    return (
        <StylesProvider jss={jss}>
            {props.children}
        </StylesProvider>
    );
}

export default RTL;