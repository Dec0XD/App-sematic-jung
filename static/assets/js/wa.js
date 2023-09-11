/**
 * A fazer:
 * pesquisar melhor forma de identificar uma jogador
 * Cálculo do sorteio baseado em frequência**/

// Número máximo de palavras sonda
const num_max_de_palavras = 10;

// Variáveis de controle
var num_de_palavras = 0;
var lista_palavras_sonda = [];
var lista_resultados = [];
var time_in = new Date;

// Array de palavras sonda selecionadas
SelectWords_cem = [
    "cabeça",
    "verde",
    "água",
    "cantar",
    "morte",
    "grande",
    "barco",
    "pagar",
    "janela",
    "querida",
    "mesa",
    "perguntar",
    "aldeia",
    "frio",
    "vara",
    "dançar",
    "lagoa",
    "doente",
    "orgulho",
    "cozinhar",
    "tinta",
    "mau",
    "agulha",
    "nadar",
    "viagem",
    "azul",
    "lanterna",
    "pecar",
    "pão",
    "rico",
    "árvore",
    "furar",
    "pena",
    "amarelo",
    "montanha",
    "morrer",
    "sal",
    "novo",
    "costume",
    "orar",
    "dinheiro",
    "besta",
    "caderno",
    "desprezar",
    "dedo",
    "caro",
    "pássaro",
    "cair",
    "livro",
    "injusto",
    "sapo",
    "partir",
    "fome",
    "branco",
    "criança",
    "atenção",
    "caneta",
    "triste",
    "uva",
    "casar",
    "casa",
    "amor",
    "copo",
    "brigar",
    "couro",
    "comprido",
    "batata",
    "pintar",
    "parte",
    "velho",
    "flor",
    "bater",
    "caixa",
    "animal",
    "família",
    "lavar",
    "vaca",
    "estranho",
    "felicidade",
    "mentir",
    "educação",
    "apertado",
    "irmão",
    "medo",
    "cegonha",
    "falso",
    "temer",
    "beijar",
    "noiva",
    "puro",
    "porta",
    "escolher",
    "grama",
    "satisfeito",
    "pirraça",
    "dormir",
    "mês",
    "chique",
    "mulher",
    "bronca"
]

// Função para obter elementos do DOM
function getElement(q) {
    return document.querySelector(q);
}

// Função para calcular a magnitude de um vetor
function mag(a) {
    return Math.sqrt(a.reduce(function (sum, val) {
        return sum + val * val;
    }, 0));
}

// Função para calcular o produto escalar entre dois vetores
function dot(f1, f2) {
    return f1.reduce(function (sum, a, idx) {
        return sum + a * f2[idx];
    }, 0);
}

// Função para calcular a similaridade de cosseno entre dois vetores
function getCosSim(f1, f2) {
    return dot(f1, f2) / (mag(f1) * mag(f2));
}

// Função para obter uma nova palavra sonda
function getNewWord() {
    const num = Math.floor(Math.random() * SelectWords_cem.length);
    const nova_palavra_sonda = SelectWords_cem[num];
    lista_palavras_sonda.push(nova_palavra_sonda);
    num_de_palavras += 1;
    getElement('#sonda').innerHTML = nova_palavra_sonda;
    time_in = new Date();
    console.log(num_de_palavras);
    console.log(nova_palavra_sonda);
    return nova_palavra_sonda;
}

// Função para obter a data atual
function getDate() {
    const now = new Date().toLocaleDateString();
    return now;
}

// Função para exibir instruções
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

// Classe para interação com o backend remoto
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

// Classe para armazenar resultados
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

// Módulo AssociaPalavra
let AssociaPalavra = (function () {
    let getModel, saveTest, backend, resultado;
    let palavra_sonda = ''; // Armazena a palavra sonda atual
    let time_out = 0; // Armazena o tempo de saída para cálculos

    async function init() {
        if (backend == undefined) {
            backend = new RemoteBackend();
        }
        getModel = backend.getModel.bind(backend);
        saveTest = backend.saveTest.bind(backend);

        palavra_sonda = getNewWord(); // Inicializa a palavra sonda

        getElement('#jump-btn').addEventListener('click', jump);

        // Recebe a palavra do usuário
        getElement('#form').addEventListener('submit', input);
    }

    async function jump(event) {
        event.preventDefault();
        time_out = new Date();
        loadTest(0, time_out, time_in, palavra_sonda, 'NaN'); // Inicia o carregamento dos testes
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

        // Verifica se a palavra inserida pelo usuário não existe no vocabulário
        if (!vetores.vec_2) {
          getElement('#word-error').innerHTML = `A palavra: ${palavra_respondida} não consta no vocabulário. Nova palavra em 2 segundos`;
          getElement("#word-error").style.display = "block";
          getElement('#sonda').classList.add('erro'); // Adiciona a classe 'erro' à palavra sonda
          time_in = new Date();
          setTimeout(() => {
            getElement('#sonda').classList.remove('erro'); // Remove a classe 'erro' após 2 segundos
            palavra_sonda = getNewWord(); // Pular para a próxima palavra sonda
            getElement('#sonda').innerHTML = palavra_sonda;
            time_in = new Date();
            getElement("#word-error").style.display = "none"; // Remove a mensagem de erro
          }, 2000); // 2 segundos de atraso
          return false;
        }

        const similaridade = getCosSim(vetores.vec_1, vetores.vec_2);
        loadTest(similaridade, time_out, time_in, palavra_sonda, palavra_respondida); // Carrega o resultado do teste

    }

    async function loadTest(similaridade, time_out, time_in, sonda, respondida) {
        const id = 0;
        const tempo_de_resposta = time_out.getTime() - time_in.getTime();
        let resultado = new Resultado(id, getDate(), tempo_de_resposta, sonda,
            respondida, similaridade);
        lista_resultados.push(resultado);
        console.log(resultado);
        const saveStatus = await saveTest(JSON.stringify(resultado));
        if (saveStatus == 500) {
            return false;
        }
        if (num_de_palavras == num_max_de_palavras) {
            endTest(); // Encerra o teste quando atingir o limite
            return false;
        }
        palavra_sonda = getNewWord(); // Atualiza a palavra sonda
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


// Evento de carregamento da página
window.addEventListener('load', async () => {

    instructions();

});
