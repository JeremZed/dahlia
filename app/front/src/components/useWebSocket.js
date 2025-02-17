import { ref, onMounted, onUnmounted } from 'vue';

export default function useWebSocket(url) {
  const socket = ref(null);
  const messages = ref([]);

  function connect() {
    socket.value = new WebSocket(url);

    socket.value.onopen = () => {
      console.log("Connecté au serveur WebSocket");
    };

    socket.value.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log("Mise à jour du monde :", data);
      messages.value.push(data);
    };

    socket.value.onclose = () => {
      console.log("Déconnecté du serveur WebSocket");
    };

    socket.value.onerror = (error) => {
      console.error("Erreur WebSocket:", error);
    };
  }

  function sendMessage(message) {
    if (socket.value && socket.value.readyState === WebSocket.OPEN) {
      socket.value.send(JSON.stringify(message));
    } else {
      console.warn("La connexion WebSocket n'est pas ouverte");
    }
  }

  onMounted(() => {
    connect();
  });

  onUnmounted(() => {
    if (socket.value) {
      socket.value.close();
    }
  });

  return { socket, messages, sendMessage };
}
