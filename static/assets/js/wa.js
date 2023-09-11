/**
 * A fazer:
 * pesquisar melhor forma de identificar uma jogador
 * Cálculo do sorteio baseado em frequência**/

const num_max_de_palavras = 10;
const total_palavras = 100;
var num_de_palavras = 0;
var lista_palavras_sonda = [];
var lista_resultados = [];
var time_in = new Date;

function getElement(q) {
    return document.querySelector(q);
}

function mag(a) {
    return Math.sqrt(a.reduce(function (sum, val) {
        return sum + val * val;
    }, 0));
}

function dot(f1, f2) {
    return f1.reduce(function (sum, a, idx) {
        return sum + a * f2[idx];
    }, 0);
}

function getCosSim(f1, f2) {
    return dot(f1, f2) / (mag(f1) * mag(f2));
}

function getNewWord() {
    const num = Math.floor(Math.random() * (total_palavras - 1)) + 1;
    const nova_palavra = SelectWords[num];
    lista_palavras_sonda.push(nova_palavra);
    num_de_palavras += 1;
    getElement('#sonda').innerHTML = nova_palavra;
    time_in = new Date();
    console.log(num_de_palavras);
    console.log(nova_palavra);
    return nova_palavra;
}

function getDate() {
    const now = new Date().toLocaleDateString();
    return now;
}

function instructions() {
    var modal = getElement("#modal");
    var span = getElement(".close");

    modal.style.display = "block";

    span.onclick = function () {
        modal.style.display = "none";
    }

    getElement('#init-btn').addEventListener('click', () => {
        modal.style.display = "none";
        AssociaPalavra.init();
    });
}
class RemoteBackend {
    async getModel(probeWord, word) {
        const url = "/model2/" + probeWord + "/" + word;
        const response = await fetch(url);
        try {
            return await response.json();
        } catch (e) {
            return null;
        }
    }

    async saveTest(dataToSend) {
        const url = "/save_test/";
        const response = await fetch(
            url, {
            credentials: "same-origin",
            mode: "same-origin",
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: dataToSend
        });
        try {
            return await response.json();
        } catch (e) {
            return null;
        }
    }
};

class Resultado {
    constructor(id, data, tempo, palavra_sonda, palavra_respondida, similaridade) {
        this.id = id;
        this.data = data;
        this.tempo = tempo;
        this.palavra_sonda = palavra_sonda;
        this.palavra_respondida = palavra_respondida;
        this.similaridade = similaridade;
    }
}

let AssociaPalavra = (function () {
    let getModel, saveTest, backend, resultado;
    let palavra_sonda = '';
    let time_out = 0;

    async function init() {
        if (backend == undefined) {
            backend = new RemoteBackend();
        }
        getModel = backend.getModel.bind(backend);
        saveTest = backend.saveTest.bind(backend);

        palavra_sonda = getNewWord();

        getElement('#jump-btn').addEventListener('click', jump);

        //recebe palavra do usuário
        getElement('#form').addEventListener('submit', input);
    }

    async function jump(event) {
        event.preventDefault();
        time_out = new Date();
        loadTest(0, time_out, time_in, palavra_sonda, 'NaN');
    }

    async function input(event) {
        event.preventDefault();
    
        time_out = new Date();
    
        getElement("#word-error").style.display = "none";
        getElement('#word').focus();
    
        let palavra_respondida = getElement('#word').value.toLowerCase();
        if (!palavra_respondida) {
            getElement('#word-error').innerHTML = `Digite uma palavra.`;
            getElement("#word-error").style.display = "block";
            time_in = new Date();
            return false;
        }
    
        getElement('#word').value = "";
        const vetores = await getModel(palavra_sonda, palavra_respondida);
        if (!vetores.vec_2) {
            getElement('#word-error').innerHTML = `A palavra: ${palavra_respondida} não consta no vocabulário.`;
            getElement("#word-error").style.display = "block";
            time_in = new Date();
            palavra_sonda = getNewWord(); // Pular para a próxima palavra sonda
            return false;
        }
    
        const similaridade = getCosSim(vetores.vec_1, vetores.vec_2);
        loadTest(similaridade, time_out, time_in, palavra_sonda, palavra_respondida);
    
    }
    

    async function loadTest(similaridade, time_out, time_in, sonda, respondida) {
        const id = 0;
        const tempo_de_resposta = time_out.getTime() - time_in.getTime();
        let resultado = new Resultado(id, getDate(), tempo_de_resposta, sonda, respondida, similaridade);
        lista_resultados.push(resultado);
        console.log(resultado);
        const saveStatus = await saveTest(JSON.stringify(resultado));
        if (saveStatus == 500) {
            return false;
        }
        if (respondida !== 'NaN') {
            num_de_palavras += 1; }
        if (num_de_palavras === num_max_de_palavras) {
            endTest();
            return false;
        }
       
        palavra_sonda = getNewWord();
        getElement('#sonda').innerHTML = palavra_sonda;
        time_in = new Date();
        return true;
    }
    
    

    function endTest() {
        console.log('end')
        getElement('#form').removeEventListener('submit', input);
        getElement('#jump-btn').removeEventListener('click', jump);
        getElement('#form').innerHTML = '';
        getElement('#sonda').innerHTML = 'O arquivo csv com o resultado do seu teste está sendo gerado.';
        const div = getElement(".btn-row");
        let fatherElement = getElement(".container");

        var _gerarCsv = function () {

            var csv = 'tempo, palavra_sonda, palavra_respondida, similaridade\n';

            lista_resultados.forEach(function (row) {
                csv += row.tempo;
                csv += ',' + row.palavra_sonda;
                csv += ',' + row.palavra_respondida;
                csv += ',' + row.similaridade;
                csv += '\n';
            });

            var fileElement = document.createElement('a', id = "file");
            fileElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
            fileElement.target = '_blank';
            fileElement.download = 'Associa_Palavra.csv';
            fileElement.textContent = "Click para baixar"
            fatherElement.appendChild(fileElement);
        };
        _gerarCsv();
    }

    return {
        init: init
    };

})();

window.addEventListener('load', async () => {

    instructions();

});
