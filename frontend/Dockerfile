FROM node:20.12.1-alpine

# Set environment variables
ENV APP_HOME /anirecs-frontend

# Set working directory
WORKDIR $APP_HOME

COPY package*.json $APP_HOME/
COPY assets/ $APP_HOME/assets/
COPY components/ $APP_HOME/components/
COPY pages/ $APP_HOME/pages/
COPY public/ $APP_HOME/public/
COPY server/ $APP_HOME/server/
COPY stores/ $APP_HOME/stores/
COPY utils/ $APP_HOME/utils/
COPY app.vue nuxt.config.ts tailwind.config.js tsconfig.json $APP_HOME/

RUN npm install

EXPOSE 3000

RUN npm run build
CMD [ "npm", "start" ]
